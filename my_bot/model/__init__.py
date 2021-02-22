# -*- coding: utf-8 -*-
from ._model import FullModel, transform
from ._download import GoogleDriveClient
from os.path import join, dirname

__all__ = ['FullModel', 'transform']

directory = join(dirname(__file__), 'tmp_weights')
downloader = GoogleDriveClient()
downloader.download_file(directory, 'deploy.prototxt')
downloader.download_file(directory, 'res10_300x300_ssd_iter_140000.caffemodel')
downloader.download_file(directory, 'deploy_age.prototxt')
downloader.download_file(directory, 'age_net.caffemodel')
downloader.download_file(directory, 'deploy_gender.prototxt')
downloader.download_file(directory, 'gender_net.caffemodel')
