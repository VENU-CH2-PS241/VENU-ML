import pandas as pd
import os

from datetime import date

from get_content_detik import scrap_detik
from get_headline_detik import get_headline_detik
from get_content_cnn import scrap_cnn
from get_headline_cnn import get_headline_cnn
from get_content_kapanlagi import scrap_kapanlagi
from get_headline_kapanlagi import get_headline_kapanlagi
from get_content_liputan6 import scrap_liputan6
from get_headline_liputan import get_headline_liputan6

def scrap():
    headline_cnn = get_headline_cnn()
    headline_detik = get_headline_detik()
    headline_kapanlagi = get_headline_kapanlagi()
    headline_liputan6 = get_headline_liputan6()

    content_cnn = scrap_cnn(headline_cnn)
    content_detik = scrap_detik(headline_detik)
    content_kapanlagi = scrap_kapanlagi(headline_kapanlagi)
    content_liputan6 = scrap_liputan6(headline_liputan6)

    return pd.concat([content_cnn, content_detik, content_kapanlagi, content_liputan6])

