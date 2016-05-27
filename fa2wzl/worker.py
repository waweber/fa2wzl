import datetime
import io

import time

from fa2wzl import compare


class Worker(object):
    def __init__(self, fa_sess, wzl_sess):
        self.fa_sess = fa_sess
        self.wzl_sess = wzl_sess

        self.folder_mapping = {}
        self.submission_folder_mapping = {}
        self.submissions_to_create = []

    def _upload_one_submission(self, sub):
        # Download the file
        # TODO: use a non protected attribute
        res = self.fa_sess._requests.get(sub.media_url)
        file = io.BytesIO(res.content)

        # TODO: not exactly the right way
        file_name_info = sub.media_url.split("/")

        file_name = file_name_info[-1]

        title = sub.title
        type = compare.convert_submission_type(sub.type)
        category = compare.convert_submission_category(sub.category)
        rating = compare.convert_rating(sub.rating)
        description = sub.description
        tags = sub.tags

        if sub in self.submission_folder_mapping:
            folder_id = self.submission_folder_mapping[sub].id
        else:
            folder_id = 0

        if type != "visual":
            # Use custom thumbnail
            res = self.fa_sess._requests.get(sub.thumbnail_url)
            thumb_file = io.BytesIO(res.content)
        else:
            thumb_file = None

        # Upload the submission

        self.wzl_sess.create_submission(
            file_name,
            file,
            title,
            type,
            category,
            rating,
            description,
            tags,
            folder_id,
            thumb_file,
        )

    def map_folders(self):
        mapping = compare.map_folders(self.fa_sess.folders,
                                      self.wzl_sess.folders)
        self.folder_mapping = {fa_folder: wzl_folder for fa_folder, wzl_folder
                               in mapping}

    def create_folders(self):
        compare.create_unmapped_folders(self.fa_sess, self.wzl_sess, list(
            (k, v) for k, v in self.folder_mapping.items()))

    def map_submissions(self):
        submission_mapping = compare.map_submissions(
            self.fa_sess.gallery + self.fa_sess.scraps,
            self.wzl_sess.gallery,
        )

        unmapped = compare.get_unmapped_submissions(
            self.fa_sess.gallery + self.fa_sess.scraps,
            submission_mapping,
        )

        folder_assoc = compare.associate_submissions_with_folders(
            self.fa_sess, unmapped,
            list((k, v) for k, v in self.folder_mapping.items()))

        self.submission_folder_mapping = {fa_submission: wzl_folder for
                                          fa_submission, wzl_folder in
                                          folder_assoc}

        self.submissions_to_create = sorted(unmapped, key=lambda x: x.id)

    def _create_all_worker(self, interval_minutes):
        for sub in self.submissions_to_create:
            if sub != self.submissions_to_create[0]:
                time.sleep(60 * interval_minutes)

            self._upload_one_submission(sub)

    def create_all(self, interval_minutes):
        self._create_all_worker(interval_minutes)
