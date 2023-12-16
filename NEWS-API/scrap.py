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

get_headline_cnn()
get_headline_detik()
get_headline_kapanlagi()
get_headline_liputan6()

today = str(date.today())

detik = 'detikNews'
cnn = 'CNNIndonesia'
kapanlagi = 'kapanlagi'
liputan6 = 'liputan6'
headline_data = os.listdir('headline')

headline_cnn = [head for head in headline_data if head.split('_')[0] == cnn and head.split('_')[-1].split('.')[0] == today]
headline_detik = [head for head in headline_data if head.split('_')[0] == detik and head.split('_')[-1].split('.')[0] == today]
headline_kapanlagi = [head for head in headline_data if head.split('_')[0] == kapanlagi and head.split('_')[-1].split('.')[0] == today]
headline_liputan6 = [head for head in headline_data if head.split('_')[0] == liputan6 and head.split('_')[-1].split('.')[0] == today]

scrap_cnn(headline_cnn)
scrap_detik(headline_detik)
scrap_kapanlagi(headline_kapanlagi)
scrap_liputan6(headline_liputan6)

