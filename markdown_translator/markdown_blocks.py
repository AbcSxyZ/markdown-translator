import copy
import hashlib

class MarkdownBlocks:
    """
    Manager for blocks of a Markdown class, containing entire markdown content.

    Store text blocks associated to their hashes, keeping the file structure
    through an hash list (in case of blocks with the same content).
    """
    def __init__(self, childrens={}, hashes=[]):
        self.childrens = childrens
        self.hashes = hashes

    def add(self, content):
        """ Add a new block of content with its associated hash. """
        block_hash = hashlib.md5(content.encode()).hexdigest()
        self.childrens[block_hash] = content
        self.hashes.append(block_hash)

    def copy(self):
        return copy.deepcopy(self)

    def pick_translations(self, translated_blocks):
        """ Select translation to insert into blocks. """
        for hash in self:
            if hash in translated_blocks:
                self[hash] = translated_blocks[hash]

    def refresh_hashes(self, selected_hashes):
        """ Replace blocks hashes with a new set. """
        if selected_hashes is None: return

        if len(self.hashes) != len(selected_hashes):
            err_msg = "Hash error: start wih {} hashes, updating {} hashes."
            raise Exception(err_msg.format(len(self), len(selected_hashes)))

        refreshed_blocks = {}
        for old_hash, new_hash in zip(self.hashes, selected_hashes):
            refreshed_blocks[new_hash] = self[old_hash]
        self.childrens = refreshed_blocks
        self.hashes = selected_hashes

    def clean(self):
        self.hashes = []
        self.childrens = {}

    def __str__(self):
        return "\n\n".join(self[hash] for hash in self.hashes)

    def __iter__(self):
        for hash in self.hashes:
            yield hash

    def __len__(self):
        return len(self.hashes)

    def __contains__(self, hash):
        return hash in self.hashes

    def __getitem__(self, hash):
        return self.childrens[hash]

    def __eq__(self, other):
        return self.hashes == other.hashes

    def __setitem__(self, hash, block_content):
        if hash not in self.hashes:
            self.hashes.append(hash)
        self.childrens[hash] = block_content

    def _hashes_render(self, hash_list):
        return "\n\n".join(self.blocks[hash] for hash in hash_list)

    def __sub__(self, old_version):
        diff_hashes = set(self.hashes) - set(old_version.hashes)
        if len(diff_hashes) == 0:
            return None

        diff_childrens = {hash: self.childrens[hash] for hash in diff_hashes}
        return __class__(diff_childrens, diff_hashes)
