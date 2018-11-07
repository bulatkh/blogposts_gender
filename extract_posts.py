import os
from mrjob.job import MRJob


class ExtractPosts(MRJob):
    """ To run these code on dataset the following command should be typed
        - python ExtractPosts.py <DATA PATH> --output <OUTPUT PATH>
    """
    post_start = False
    post = []

    def mapper(self, key, line):
        """ parse each line of text"""
        filename = os.environ["map_input_file"]
        # get gender from the filename
        gender = filename.split(".")[1]
        # parse line
        line = line.strip()
        if line == "<post>":
            self.post_start = True
        elif line == "</post>":
            self.post_start = False
            # yield gender and post
            yield gender, repr("\n".join(self.post))
        elif self.post_start:
            self.post.append(line)


if __name__ == '__main__':
    ExtractPosts.run()