from cadnano.cnproxy import UndoCommand
from cadnano.strand import Strand
import cadnano.preferences as prefs
import random

class RemoveStrandCommand(UndoCommand):
    """
    RemoveStrandCommand deletes a strand. It should only be called on
    strands with no connections to other strands.
    """
    def __init__(self, strandset, strand, solo=True):
        """
        Args:
            strandset (StrandSet):
            strand (Strand):
            solo (Optional[bool]): set to True if only one strand is being
                removed to minimize signaling
        """
        super(RemoveStrandCommand, self).__init__("remove strands")
        self._strandset = strandset
        self._strand = strand
        self._solo = solo
        self._old_strand5p = strand.connection5p()
        self._old_strand3p = strand.connection3p()
        self._oligo = olg = strand.oligo()

        part = strand.part()
        idxs = strand.idxs()
        self.mids = (   part.getModID(  strand, strand.lowIdx()),
                        part.getModID(strand, strand.highIdx()) )

        # only create a new 5p oligo if there is a 3' connection
        self._new_oligo5p = olg.shallowCopy() if self._old_strand5p else None
        if olg.isLoop() or self._old_strand3p is None:
            self._new_oligo3p = olg3p = None
            if self._new_oligo5p:
                self._new_oligo5p.setLoop(False)
        else:
            self._new_oligo3p = olg3p = olg.shallowCopy()
            olg3p.setStrand5p(self._old_strand3p)
            # color_list = prefs.STAP_COLORS if strandset.isStaple() else prefs.SCAF_COLORS
            color_list = prefs.STAP_COLORS
            color = random.choice(color_list)
            olg3p.setColor(color)
            olg3p.refreshLength()
    # end def

    def redo(self):
        # Remove the strand
        strand = self._strand
        strandset = self._strandset
        doc = strandset._document
        doc.removeStrandFromSelection(strand)
        strandset._removeFromStrandList(strand)

        strand5p = self._old_strand5p
        strand3p = self._old_strand3p
        oligo = self._oligo
        olg5p = self._new_oligo5p
        olg3p = self._new_oligo3p

        #oligo.incrementLength(-strand.totalLength())
        oligo.removeFromPart()

        if strand5p is not None:
            strand5p.setConnection3p(None)
        if strand3p is not None:
            strand3p.setConnection5p(None)

        # Clear connections and update oligos
        if strand5p is not None:
            for s5p in oligo.strand5p().generator3pStrand():
                Strand.setOligo(s5p, olg5p)
            olg5p.refreshLength()
            olg5p.addToPart(strandset.part())
            if self._solo:
                part = strandset.part()
                id_num = strandset.idNum()
                # Why is this signal emitted here?
                part.partActiveVirtualHelixChangedSignal.emit(part, id_num)
                #strand5p.strandXover5pChangedSignal.emit(strand5p, strand)
            strand5p.strandUpdateSignal.emit(strand5p)
        # end if
        if strand3p is not None:
            if not oligo.isLoop():
                # apply 2nd oligo copy to all 3' downstream strands
                for s3p in strand3p.generator3pStrand():
                    Strand.setOligo(s3p, olg3p)
                olg3p.addToPart(strandset.part())
            if self._solo:
                part = strandset.part()
                id_num = strandset.idNum()
                part.partActiveVirtualHelixChangedSignal.emit(part, id_num)
                # strand.strandXover5pChangedSignal.emit(strand, strand3p)
            strand3p.strandUpdateSignal.emit(strand3p)
        # end if
        # Emit a signal to notify on completion
        strand.strandRemovedSignal.emit(strand)

        if self.mids[0] is not None:
            strand.part().removeModStrandInstance(strand, strand.lowIdx(),
                                                    self.mids[0] )
        if self.mids[1] is not None:
            strand.part().removeModStrandInstance(strand, strand.highIdx(),
                                                            self.mids[1])

        # for updating the Slice View displayed helices
        strandset.part().partStrandChangedSignal.emit(strandset.part(),
                                                        strandset.idNum())
    # end def

    def undo(self):
        # Restore the strand
        strand = self._strand
        strandset = self._strandset
        doc = strandset._document
        # Add the new_strand to the s_set
        strandset._addToStrandList(strand)
        strand5p = self._old_strand5p
        strand3p = self._old_strand3p
        oligo = self._oligo
        olg5p = self._new_oligo5p
        olg3p = self._new_oligo3p

        # Restore connections to this strand
        if strand5p is not None:
            strand5p.setConnection3p(strand)

        if strand3p is not None:
            strand3p.setConnection5p(strand)

        # oligo.decrementLength(strand.totalLength())

        # Restore the oligo
        oligo.addToPart(strandset.part())
        if olg5p:
            olg5p.removeFromPart()
        if olg3p:
            olg3p.removeFromPart()
        for s5p in oligo.strand5p().generator3pStrand():
            Strand.setOligo(s5p, oligo)
        # end for

        # Emit a signal to notify on completion
        strandset.strandsetStrandAddedSignal.emit(strandset, strand)

        if self.mids[0] is not None:
            strand.part().addModStrandInstance(strand, strand.lowIdx(),
                                                self.mids[0])
            strand.strandModsAddedSignal.emit(strand, self.mids[0],
                                                strand.lowIdx())
        if self.mids[1] is not None:
            strand.part().addModStrandInstance(strand, strand.highIdx(),
                                                self.mids[1])
            strand.strandModsAddedSignal.emit(strand, self.mids[1],
                                                strand.highIdx())

        # for updating the Slice View displayed helices
        strandset.part().partStrandChangedSignal.emit(strandset.part(),
                                                        strandset.idNum())

        # Restore connections to this strand
        if strand5p is not None:
            if self._solo:
                part = strandset.part()
                id_num = strandset.idNum()
                part.partActiveVirtualHelixChangedSignal.emit(part, id_num)
                # strand5p.strandXover5pChangedSignal.emit(
                #                                        strand5p, strand)
            strand5p.strandUpdateSignal.emit(strand5p)
            strand.strandUpdateSignal.emit(strand)

        if strand3p is not None:
            if self._solo:
                part = strandset.part()
                id_num = strandset.idNum()
                part.partActiveVirtualHelixChangedSignal.emit(part, id_num)
                # strand.strandXover5pChangedSignal.emit(strand, strand3p)
            strand3p.strandUpdateSignal.emit(strand3p)
            strand.strandUpdateSignal.emit(strand)
    # end def
# end class
