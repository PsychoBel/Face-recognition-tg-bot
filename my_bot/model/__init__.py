# -*- coding: utf-8 -*-
from ._model import FullModel, transform
from ._download import GoogleDriveClient

__all__ = ['FullModel', 'transform']

downloader = GoogleDriveClient()
downloader.download_file('../tmp_weights', 'deploy.prototxt')
downloader.download_file('../tmp_weights', 'res10_300x300_ssd_iter_140000.caffemodel')
downloader.download_file('../tmp_weights', 'deploy_age.prototxt')
downloader.download_file('../tmp_weights', 'age_net.caffemodel')
downloader.download_file('../tmp_weights', 'deploy_gender.prototxt')
downloader.download_file('../tmp_weights', 'gender_net.caffemodel')
