"""
Extract and organize test images from TC-H01 to TC-H20
Downloads and saves images in data/inputs and data/outputs folders with descriptive naming
"""

import os
import requests
from pathlib import Path
from urllib.parse import urlparse
import time
import warnings
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Test case data with image URLs
test_cases = {
    "TC-H01": {
        "description": "red_sleeveless_dress",
        "text_query": "red floral party dress",
        "inputs": [
            "https://images.openai.com/static-rsc-3/wJJJxl2cP3mrHgJtE4diNGSbtTffAV8R32FDs5vI2vK6KLBrS02XF2McUVej9f68Gjbd5h8-uVCT8qHDZD8GRUiCfdRzVKLTp6dm7BOjzds?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/NMdjKI52EGvc6pyFViTPLv4pOJM_fUJe86DgYU38_jUTPr-O1cuvBTONdgyeYld_qlClAHs9mmHOoyljCttXFhv1UEXrKX5bHpHh4k608sk?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/fF62REnuaWbDhrs1nvsNcKdPsyoIjUwrdb6UyNcRZWna4_xWPPf4MABtCt7SFJAkp9Sht1p3TPMspzUJxXzlVT6d9TNrKo5ec7R_Or8UPXI?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://dimpledesignstudio.com/cdn/shop/files/MAK6552-Custom.jpg?v=1706137885",
            "https://uandf.co.in/cdn/shop/files/DD19688-330_1.jpg?v=1720615770&width=1080",
            "https://www.kissprom.com/cdn/shop/files/luxurious-a-line-quinceanera-dress-ball-gown-sweet-16-dress.png?v=1740902284"
        ]
    },
    "TC-H02": {
        "description": "blue_denim_jacket",
        "text_query": "formal office blazer",
        "inputs": [
            "https://images.openai.com/static-rsc-3/l2IDyJcfoc6NsX_jJFP0uNB2JTzWmaL_A8vxH8JFv8CxumV6YJDFjM-01pdH24mZd9ywSEKI0EeNiCy-oszVL870RObnYyKBpWaaVUlPR4Q?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/nUEqqZ3DTtxR-shBbWt0oRYFwjoK49rRXf0Kt_dFZXXMbP-yYSbqvuF3nT7FHOb_zCi6corfBhCpvtcgTgoJvU1reIG5TWxvlqXXPG_u1qg?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/utcUu3foIXbdvAXZk6TB5es7DcMmhhKd6kGcHxQAYKDBDytp_dc5y2aAnY1nfv5FYlMtOFfwsSrBqKlKy_yVsAlYVgi5bccev9193aUPpE4?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://sunantamadaan.com/cdn/shop/files/Royal_Blue_Color_Blazer_Set.jpg?v=1737817929",
            "https://m.media-amazon.com/images/I/71chVkHUPSL._AC_UY1100_.jpg",
            "https://dheerajsharma.com/cdn/shop/files/Task-31138631-1-1.png?v=1739805326"
        ]
    },
    "TC-H03": {
        "description": "black_plain_tshirt",
        "text_query": "black graphic streetwear t shirt",
        "inputs": [
            "https://images.openai.com/static-rsc-3/tXyKu_zrIN3hZYPuie7orvMeWf4agKN5P5QAUITL6RcdbuP4KdgEoX9BC79ySK-CkKCiqEsTp_O7s2tc8R8p9WTmMiwqqUuAJnS7R1uGOW4?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/jHlWTxUywooZk1B6fO9mTAZu8QoSIdxmM9xyN83et36cRTHLxsne_P-_OuQGtqO4n1XYYY8HZvwG8D-ph2ARK_jm8Zd2k5U28HRAi5TZ2oc?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/ibJuY0c6RechvUajX9rDeyTmqjoDIGhUpwbe7ABR9w3g36OUZT2AtgSzI4ZHMqoDvMid6SItbr5o2lsECAeJTo9Dn75ayw0KNSFLaRdR_qw?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://veirdo.in/cdn/shop/files/b_0119493a-9927-4550-8323-baefe5f625c0.jpg?v=1759917565",
            "https://www.instinctfirst.com/cdn/shop/files/ClassicBlackfront.png?v=1704186208&width=640",
            "https://campussutra.com/cdn/shop/files/CSMSSRT8041_1_7e21e01e-95bb-41a1-b851-4197185df534.jpg?v=1734420299"
        ]
    },
    "TC-H04": {
        "description": "green_silk_saree",
        "text_query": "traditional wedding outfit",
        "inputs": [
            "https://sushmi.studio/cdn/shop/files/145B2595-DC46-4AF6-ACC2-47FB5CD97E5B_2000x.jpg?v=1762797962",
            "https://assets0.mirraw.com/images/5936721/image_zoom.jpeg?1538498356=",
            "https://sitahethnic.com/cdn/shop/files/9C187676-AE52-4021-9965-B11849213493.jpg?v=1755612064"
        ],
        "outputs": [
            "https://assets0.mirraw.com/images/11906301/Green_%281%29_zoom.jpg?1696064164=",
            "https://i.pinimg.com/736x/2a/7f/c5/2a7fc5cea30c820b0dfcec628ac9293d.jpg",
            "https://assets0.mirraw.com/images/10004799/7402-3_zoom.jpg?1696933142="
        ]
    },
    "TC-H05": {
        "description": "white_sneakers",
        "text_query": "black leather formal shoes",
        "inputs": [
            "https://images.openai.com/static-rsc-3/Ab2mlLIXJfFJSpBa2qqO5S3-faIVPR2eiPVN-tmBqkIs4FZqm5YJItO9-qf4tF81P7QvrGiArwORf0NYp7WRHbiG2kmr3HIPde5AAKRhscs?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/q87hndzrBRamQt1EbZEtHxvHkUTLhznfBXL8e2gTE2ab8VSpCEk3ZcysaZUM7GP_6nVX72Epwd5BLHPRHlenVcKteLIlAA2JwVdFgfDgXxg?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/MZaE4clIzb1TNJUtW0pPGEgyEHN3wR2AQRM9fhXWX4AumeWgVUjKIgwYJES0wyxQG4_UQHH5dqnzrvFF__7DYlhS4_p5hJLb-4p8ZQ9ChLs?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://hitz.co.in/cdn/shop/files/6344-BLACK.jpg?v=1755619053",
            "https://xcdn.next.co.uk/common/items/default/default/itemimages/3_4Ratio/product/lge/C28489s.jpg?im=Resize%2Cwidth%3D750",
            "https://paragonfootwear.com/cdn/shop/products/K11239G_BLK_1.jpg?v=1756713401"
        ]
    },
    "TC-H06": {
        "description": "grey_hoodie",
        "text_query": "winter street fashion hoodie",
        "inputs": [
            "https://images.openai.com/static-rsc-3/eK2hH70SUbpCnWoy1k3dnmdg68YQdRQE-MOCgSEzo6ZKITSJv-RolKha-tbh7nQTtGnA_8Q9zKC0ke5FITiXGESXjCxXd3lAlmEEDAdmJfU?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/256yloByccTcYBSAHA6nfQzrE5FbXhDoArC5BoeP2flY2txPWid31AqlzRkBmdlQYn8ZVn3vYZttysw19oumEgPjvX7Q_FnYVHYxPQkPPH0?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/8Oxidl5nVgIox9LOMWCiwMBpciFQEhdiE7v9rO0nWBZwJIJuHldt6fDUsveeZNonuKXrSw_tRJePkw6Uboh4vaGwv5N679stUNWkKW1e5Hw?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://nobero.com/cdn/shop/files/Go_through_front.jpg?v=1732862026",
            "https://i.pinimg.com/736x/90/7a/9d/907a9d26591405a8523209fcdf7047d8.jpg",
            "https://m.media-amazon.com/images/I/71mvuPdMmOL._AC_UY1100_.jpg"
        ]
    },
    "TC-H07": {
        "description": "yellow_kurti",
        "text_query": "festive embroidered kurti",
        "inputs": [
            "https://images.openai.com/static-rsc-3/2thkQst837BPpK_T31lGvAW4AnhyGlwwzwXsZRxuqPlpygmFv6fyQwY9SgVOHmSvGnYj8AtlRQS7oywJmzZebkK6qo1JNRG7ny3jX6k01HI?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/2wVwIumioH2SGcjfPNxFd1WE4M_CpgnRWM62RIaUOrihcWQSuNxTabWT1h6igKcQ-fihp4YtgVmx0hLtceixU7rGeCB2x2w8_f9E1pkUp8Q?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/MYNFuqldx7WW_rlT_ibCLt1_su5xOVxttgctecjlo49isjbQJ1W12VNJO-MsNmz6ogY2hrW5d9eYqGnZnGxjtDkY2RZWtoCpUj3jf6Gu1CY?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://www.royalexport.in/product-img/festive-yellow-embroidered-kur5-1734080514.jpg",
            "https://images.openai.com/static-rsc-3/6XsHgMw3O5zFM-pQJzdf6Mt-Cj_xsT0QF8m0Khy6qo3samiHXJibXUZEHA4_kCXeAnJQZM4mYmwzUVxf2HCi-O7wD24hO4UDiV-I2Jc657M?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/D_OXRtAqIq3hkt7cEEx3MAmhP57hrfFRjpsmsbSKDm8ZTdM8jKTdzUo_AklT_04ogX8PZyuD5Dbmj4gbSTjXj3ZbYmoYUcrTOR5ea3PtGEo?purpose=fullsize&v=1"
        ]
    },
    "TC-H08": {
        "description": "black_blazer",
        "text_query": "smart casual evening outfit",
        "inputs": [
            "https://images.openai.com/static-rsc-3/VESrdLSWpHUGkFUB6a54wz9LlREXRI8e1604SHH3Am4Bi15FpjG5BfQw7pcLoEWdRPDfl06ETbxLAX5_Po-T9h5HSbXeqaUysmWL5giLJZk?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/1010IkxUNGlvjh1nTVV_kKoiKSztqlL_WRZbNAmijvxNfMPwtfvFmO69whVR29GNg26foNUuoZZiKiYE0oUiJ9Jd3uPuavthZIe77qSNTVg?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/D3HuYgVPwCaos3MXEsKV-xlqabc82oySPoTh5sIZ_UYxbxlfsze_tpmhDsPHT6_go2NwIhPkA20lJT6iRxEP5HABfUGT3Cmkj88JTVIhHNw?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://imagescdn.louisphilippe.com/img/app/product/7/775602-14703284.jpg?auto=format&w=390",
            "https://i.pinimg.com/736x/2b/de/a4/2bdea4f410a258ee0b91cbe83af6a014.jpg",
            "https://images.meesho.com/images/products/445011569/tic8r_512.webp?width=512"
        ]
    },
    "TC-H09": {
        "description": "white_shirt",
        "text_query": "lightweight summer shirt",
        "inputs": [
            "https://images.openai.com/static-rsc-3/lPLkK01VQ0AJkfrq1dXAhsJi-NOTNUXW3CsUQ6MHOyahSE-yrDCEIcgfNNRf7Cv2aS9EZFt7aQ2y5K-K56A5hX0y1H0kx4aEa4m85wnJpwY?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/8pmzq9ybcGkaB93z_mSqiSGK9SktNqb5vaVip4Uai6-ic9sB9OtpZdoJqiZ9ySqAkB8uNr0JuuenR-MQJodtj7zOK6BkYO7V1cRcJ5FYmFQ?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/er8dDuq1WpcVq1mRX1X6IQx9PLqgHFAVlA9LeB6XhfxhbdkDGf07cvYEeC8laCfSGw3mJJ1VJK5ZPFe_Di-mlJ7-__hBwLbgzfB5mzhl-ZI?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://cdn2.propercloth.com/pic_cs/984ca500a4f31a4d2c5737da15176572_size6.jpg",
            "https://successmenswear.com/cdn/shop/products/IMG_6067.jpg?v=1663403188",
            "https://m.media-amazon.com/images/I/71Re2d3PWwL._AC_UY1100_.jpg"
        ]
    },
    "TC-H10": {
        "description": "pink_midi_dress",
        "text_query": "elegant wedding guest outfit",
        "inputs": [
            "https://images.openai.com/static-rsc-3/-Oid2sXBscJCUDAiWmsEOMKrbffko2_pGqg61EgGK9CjkoaQiEyYCA0psWro8g6sGaNHF7618rtuRx59l4dCS7NLi133xQxL06ClPExqISA?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/WsMZIXnFP4tL2yxGHBqdEKorQApsJ5Q6RVSc8jz1iYTt_cxgZOMQZa8NB_1sbQSSI_ItU-7sKsTi_8cWA8RiILqnxJ5aQGZMVd2QcaOKcDI?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/m8L1SgE17hGH1mLJEyLpBJ8YYpr_mvlZLAPMHRKdTVoNs0xe1qad1DetIY7hT_aSt4acouDzNcXhVhaiUou3qqRpN6NnIS9w3mkP2YBuR8c?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://i.pinimg.com/736x/7c/67/27/7c6727305a490ff9d088f293eccb6115.jpg",
            "https://i.pinimg.com/564x/18/ea/39/18ea391c25794379446a083b03bd2d07.jpg",
            "https://images.openai.com/static-rsc-3/LRqAS3P8lWHjipf9kflOMKUNP9IbbAKdupImCeXD5rUsdTnhIWHl3Dc6Zpmuln_xq07yRXnQTw5x0djDFR2BnSvYM3fsk2zi1p02hPvqQJs?purpose=fullsize&v=1"
        ]
    },
    "TC-H11": {
        "description": "brown_boots",
        "text_query": "hiking outdoor footwear",
        "inputs": [
            "https://images.openai.com/static-rsc-3/-ZuZo3j0mOOlmy-VYpX7R6tiMEw817of8V5VZ_Lfvvg4k58bMENC_tmN1oy-dIAc6HPE_qgaHstFQiWPkzmfzjLeMrFXNwDuMt8k8SOZ8Ms?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/-ST79FJxtEyCZWecg5rTmdJHx0Rx34uQeL7aJhwf485gyythbTpfN4eI02BYSJhGHDO90ZgbpiBo1wk79cf8EYdz7AorTobZab2R2L-zHN4?purpose=fullsize&v=1",
            "https://tiimg.tistatic.com/fp/1/009/938/leather-boots--515.jpg"
        ],
        "outputs": [
            "https://cdn.runrepeat.com/storage/gallery/buying_guide_primary/100/100-best-leather-hiking-boots-21273743-main.jpg",
            "https://d1i8d6ce8wwubf.cloudfront.net/photos/33/21/453596_26533_XXL.jpg",
            "https://m.media-amazon.com/images/I/71OxTkqFT4L._AC_UY1000_.jpg"
        ]
    },
    "TC-H12": {
        "description": "blue_jeans",
        "text_query": "ripped distressed street style jeans",
        "inputs": [
            "https://images.openai.com/static-rsc-3/BAe8n3aLfpj_T_idIW7j_MpcAl2nMaZyXCKb9de5LOhkOsSlYybubjIBfHrttjsTlr5st5IBvtj-gT8OEBSDn41ve2JV8DIncK3iXQlr_6k?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/e9bbWCQ4rploPQF2sku4ZAyETG0VP-ANh-4gn1R5SWVDxACrKmCJNjA3S5GJjd_RNS3uDN3E97Le8qJ8rfIDx9mU6qEHlARF0vhHLOFuOiI?purpose=fullsize&v=1",
            "https://www.rogic.in/cdn/shop/files/9806S_1_61f3c0a2-3491-4e80-ab21-beccc99705d9.jpg?v=1725454507&width=1080"
        ],
        "outputs": [
            "https://images.openai.com/static-rsc-3/eTqHQK24A_3xT5NsOKefmZik_T8BiTINj7frPwUzoz6rvWLObj5RtV5nSfIUHwiLNBus-wkhcM1EolQXgu2iiGpzKDcA3Uo3Koi-zo3c00k?purpose=fullsize&v=1",
            "https://i.pinimg.com/564x/60/b4/84/60b484ef2f83f79197920ffc3d7167c1.jpg",
            "https://cdn-img.prettylittlething.com/4/7/d/a/47da73bafa3fb825bb8f471d55bb8375f78e0d3f_cms6113_5.jpg"
        ]
    },
    "TC-H13": {
        "description": "black_saree",
        "text_query": "reception party wear saree",
        "inputs": [
            "https://studiosy.in/cdn/shop/files/Chaavi_-75_1.jpg?v=1709021040",
            "https://assets2.andaazfashion.com/media/catalog/product/p/l/plain-chiffon-black-party-wear-saree-sarv123015-1.jpg",
            "https://images.openai.com/static-rsc-3/NAytzYJT73_vyudJXhWhVGx_o5O1uIyL8aUNNKbrbiwGD7Pz-ZZWzMNLEgu07SpA6x-aEQ90Xoxh2TQF_qa0VApayDQsw3OtVHeiD0Dcrn0?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://mysilklove.com/cdn/shop/files/9_f7469b18-b782-4e05-8ea0-c68be7f17e09.jpg?v=1736848155&width=2048",
            "https://fabvilla.in/cdn/shop/files/IMG_7693_668fb5d0-e751-4dd4-897a.jpg?v=1743849346",
            "https://img.perniaspopupshop.com/catalog/product/a/r/ARRA112222_1.jpg?impolicy=detailimageprod"
        ]
    },
    "TC-H14": {
        "description": "green_tshirt",
        "text_query": "gym fitness performance t shirt",
        "inputs": [
            "https://images.openai.com/static-rsc-3/YBW63tUqW4Siiskf8mIsl9t8zhvuZA5MD4rST0lKHoIWK9XtAPRz0NMuP0Fuf3K-hqgrdoEjQykqZOxIL14QfoD7WW89trYTu8mOnDs1Bz8?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/ZO_PLksbhiPBKL0My1UZS8Ub1kKvL5_c7mRoB4QZM1D6a7jWK6U5TQRdNAx1_B6lB2nHseEUIRO58V9dkLu0x0ejnMKuokp-pTKq6t0upMM?purpose=fullsize&v=1",
            "https://www.shopghumakkad.com/cdn/shop/files/dark-green-t-shirt-for-men-ghumakkad-1_1800x1800.jpg?v=1741450592"
        ],
        "outputs": [
            "https://www.gorillawear.com/resize/90515409-performance-t-shirt-army-green-8_16895014445696.jpg/0/1100/True/performance-t-shirt-army-green-3xl.jpg",
            "https://m.media-amazon.com/images/I/71KLxoh43OL._AC_UY1000_.jpg",
            "https://chkokko.com/cdn/shop/files/Bottle_Green_T_01.jpg?v=1735383679"
        ]
    },
    "TC-H15": {
        "description": "white_heels",
        "text_query": "bridal wedding heels elegant",
        "inputs": [
            "https://images.openai.com/static-rsc-3/3x2UJqzdv7oK8VL1HTl2YtoBOTR8BusHmalTNXKi2uddqQbYZ2xb08p2a0T4v0tPOllsntPsaj4AnzNaH8Kesa1V4lQfaLmf569lpifYha0?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/YEMFT-tBwxb8Nzt-1lBEWBfjohLfFmqb3BH3zPjlgLl_bLMNC0J5tDLpyY5QTqxUxSC9kxj7ijUBj7YBOIQF_OLCMsJYyMaPdGkTW84jnWI?purpose=fullsize&v=1",
            "https://n.nordstrommedia.com/it/e01a4f9f-d403-4e20-ae88-42c041290b92.jpeg?dpr=2&h=368&w=240"
        ],
        "outputs": [
            "https://images.openai.com/static-rsc-3/DOfxX3jTYpX-DZDGwUw0tQHf-2tihNbvNVvqteI6NxeBz72qZ_VfUeaK8yiOVnq_W1CARNWPkej8Wshp71k92CsFyOi9EdhpeCxl_Co5AkQ?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/jvbluppBkNmAgfCKbK2E6vZLVOmSTqtR53_Lc_jkvNLRXPpPXJ2McICLAIMdKJdi6BmSoFtwNbo1b1-cPcxNsAIayzQtl_x0ZDf2lNZCmAg?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/T4puuODMoAdligXuEUwb4tkTBAuY3Npjjxx7yOAO_b-OyWvkYpVhdrfPHJUW3wavoVxRsgg-QpHrOkLal7rlvVfa9eE60fFGqLzBJkeA164?purpose=fullsize&v=1"
        ]
    },
    "TC-H16": {
        "description": "leather_jacket",
        "text_query": "biker street fashion jacket",
        "inputs": [
            "https://images.openai.com/static-rsc-3/3CDTL-rzNP0bqCYzq0vRGUzoCiDK1sLObV2qSmMSdGZwrTsGheDU1PZCNytiGLX2sAydXO1bVWZjVTz2IBICN-PSmyxRe3ja078ylI4j31E?purpose=fullsize&v=1",
            "https://m.media-amazon.com/images/I/617qtPqTsNL._AC_UY1000_.jpg",
            "https://images.openai.com/static-rsc-3/fbjtwW2LKoWdv7JiSo0llc1IF3vo94GAQWFHdEgzd99nKgR-gE8dXkXpuYX6vppWnudmKlTC2Citqb8LNkj9-iVTiYsu8u6LYaWaD1KIf9c?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://i.ebayimg.com/images/g/vXgAAOSwxetje9uR/s-l1200.jpg",
            "https://cdn.mos.cms.futurecdn.net/whowhatwear/posts/311578/french-girl-black-leather-outfit-ideas-311578-1704777076285-square.jpg",
            "https://thursdayboots.com/cdn/shop/products/1024x1024-Moto-BlackMatte-Black-011723-3_1024x1024.jpg?v=1714000290"
        ]
    },
    "TC-H17": {
        "description": "floral_skirt",
        "text_query": "summer beach vacation outfit",
        "inputs": [
            "https://images.openai.com/static-rsc-3/hQzYHRd2f-nnAvS7fzw42QoqdQn4anf_xNjj3qEFzRGdctPl5-kV9KT8cZgwduzcw4w0JNKtrCLBepfWfOL_KnGsY-GMGwUpfrx2nh4QYgg?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/j7We0KE_Sih2ShN_C5vZ3yPSAQJJgpfIUbt1nFFVXAara2NZMMBh37Pcmz74NhOiLfr7mFTzj_OCxBUFtXIKj6bOnF-Bjw3Ic4NAR224YLY?purpose=fullsize&v=1",
            "https://solstudio.in/cdn/shop/files/Untitleddesign_3.png?v=1726139562&width=1946"
        ],
        "outputs": [
            "https://m.media-amazon.com/images/I/81wYyxD2AUL._AC_UY1100_.jpg",
            "https://www.thebeachcompany.in/cdn/shop/files/Beach-Skirt-Wrap-Skirt-Retro1_2400x.webp?v=1751526529",
            "https://m.media-amazon.com/images/I/71byN2%2B7sJL._UY1000_.jpg"
        ]
    },
    "TC-H18": {
        "description": "navy_suit",
        "text_query": "formal job interview suit",
        "inputs": [
            "https://images.openai.com/static-rsc-3/w75-g32rJyYaYuflwvaZQ_RcKfg5urwDmOPUJaufNSs6aTteJ1P2MPK2kOEIHP3cC_FA0s1c69zW4aLTPLFHRCuS-_91LEdsIr17RBevL0s?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/bdwcnJmbgJ4nDTUt1HgARIcAihpf-OqeydoQp34We40yk0oBsFh18PX77LnSJREeEdOuna12MFyMRhXHa4Hk6W0QaFRch-80GYds-NQB0bg?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://theblacktux.com/cdn/shop/articles/what-to-wear-to-a-job-interview-make-the-perfect-first-impression-160587.png?v=1742530405&width=480",
            "https://images.openai.com/static-rsc-3/bdwcnJmbgJ4nDTUt1HgARIcAihpf-OqeydoQp34We40yk0oBsFh18PX77LnSJREeEdOuna12MFyMRhXHa4Hk6W0QaFRch-80GYds-NQB0bg?purpose=fullsize&v=1",
            "https://thesuitdepot.com/cdn/shop/products/raphael-two-piece-suits-36s-men-s-raphael-slim-fit-solid-navy-blue-two-button-wool-formal-business-suit-508-2-sf-36s-29536477282486.jpg?v=1691515276"
        ]
    },
    "TC-H19": {
        "description": "red_hoodie",
        "text_query": "sports activewear hoodie",
        "inputs": [
            "https://images.openai.com/static-rsc-3/UCFeBwJoqyQGO32f-vzmZss4aPrXMgk6Rmqm4zEOJhI0LhvxS1APS2EpiyFGA7d6p1d98uAdGylOzQzzmaUuSSmKAOtpTWsFQ-dX5VybW5s?purpose=fullsize&v=1",
            "https://m.media-amazon.com/images/I/51tEciwZARL._AC_UY1000_.jpg",
            "https://images.openai.com/static-rsc-3/eKC-A4rIP7RcEdJgKkEr3w6ps8UohGXe_cJA2skHEKSAgH1T-bZhV6GaIsEfmaepKUKJXCETSRMdy5sc9QZjCOwNQ82eM-sE7DaPjvfO7pw?purpose=fullsize&v=1"
        ],
        "outputs": [
            "https://m.media-amazon.com/images/I/71J1WNxxyEL._AC_UY1000_.jpg",
            "https://assets.ajio.com/medias/sys_master/root/20230213/52Xq/63ea4fa0f997dde6f4a20e31/-473Wx593H-410354024-17i-MODEL.jpg",
            "https://i.ebayimg.com/images/g/As0AAOSwbq5irj~g/s-l1200.jpg"
        ]
    },
    "TC-H20": {
        "description": "beige_coat",
        "text_query": "luxury winter overcoat premium",
        "inputs": [
            "https://images.openai.com/static-rsc-3/-F1HmHypztw4tjaMmZtpx42T3t3zboEXJD37orrhUvLjmwupbPiK881rb3wk-g9d77dXtVbbPMRNDjBBZssCAxsqzckW549DMM-Igkh9-Z4?purpose=fullsize&v=1",
            "https://images.openai.com/static-rsc-3/2lAXk1Xim7zJeTegOyuMnl10WRpML7levnoOUIp-uAVYXBP_qz6ojgsMCPyJ79CQgimVbhdFcJcdBQtQQRqAifb_f1BaCskpgYv9O3ZZpMo?purpose=fullsize&v=1",
            "https://attirethestudio.com/cdn/shop/files/WoolTrenchCoatBeige_800x.jpg?v=1698763996"
        ],
        "outputs": [
            "https://us.herno.com/dw/image/v2/BGRP_PRD/on/demandware.static/-/Sites-33/default/dw8ba76396/images/zoom/CA000544D33313_1980_1.jpg?sh=475&sm=fit&sw=375",
            "https://i5.walmartimages.com/seo/Aayomet-Womens-Coat-Women-s-Hooded-Parka-Coat-Winter-Coats-Warm-Jacket-Long-Parka-Coat-Thichkened-Winter-Jacket-with-Pockets-Beige-L_61089094-4f2e-45e0-9b28-a530842f7f78.326d0df98181f189a5b36f501f92cf30.jpeg?odnBg=FFFFFF&odnHeight=768&odnWidth=768",
            "https://us.akris.com/cdn/shop/files/img_54335d1f-6eb7-44d4-9ae4-fe96ee1994f8.png?v=1755083633&width=1200"
        ]
    }
}

def get_file_extension(url):
    """Extract file extension from URL"""
    # Remove query parameters
    url_without_params = url.split('?')[0]
    # Get the last part of the path
    path = urlparse(url_without_params).path
    if '.' in path:
        return '.' + path.split('.')[-1]
    return '.jpg'  # Default to jpg

def download_image(url, filepath, max_retries=3):
    """Download image with retry logic"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=20, verify=False)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✓ Downloaded: {filepath}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"⚠ Attempt {attempt + 1} failed for {url}: {str(e)[:80]}")
            time.sleep(3)  # Wait before retrying
    
    print(f"✗ Failed to download: {url}")
    return False

def main():
    """Main function to organize and download images"""
    
    # Create base data directory
    base_dir = Path(r"s:\Siddu\Final Year\cross-modal-recommendation-system\data")
    inputs_dir = base_dir / "inputs"
    outputs_dir = base_dir / "outputs"
    
    # Create directories
    inputs_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("EXTRACTING AND ORGANIZING TEST IMAGES")
    print("=" * 80)
    
    total_images = 0
    successful_downloads = 0
    
    # Process each test case
    for tc_id, tc_data in sorted(test_cases.items()):
        print(f"\n📦 Processing {tc_id}: {tc_data['description']}")
        print(f"   Query: {tc_data['text_query']}")
        
        # Download input images
        print("   📥 Input Images:")
        for idx, url in enumerate(tc_data['inputs'], 1):
            ext = get_file_extension(url)
            filename = f"{tc_id}_input_{tc_data['description']}_{idx}{ext}"
            filepath = inputs_dir / filename
            
            # Skip if already exists
            if filepath.exists():
                print(f"✓ Already exists: {filename}")
                continue
            
            if download_image(url, filepath):
                successful_downloads += 1
            total_images += 1
        
        # Download output images
        print("   📤 Output Images:")
        for idx, url in enumerate(tc_data['outputs'], 1):
            ext = get_file_extension(url)
            filename = f"{tc_id}_output_{tc_data['description']}_{idx}{ext}"
            filepath = outputs_dir / filename
            
            # Skip if already exists
            if filepath.exists():
                print(f"✓ Already exists: {filename}")
                continue
            
            if download_image(url, filepath):
                successful_downloads += 1
            total_images += 1
        
        time.sleep(2)  # Be respectful to servers
    
    # Print summary
    print("\n" + "=" * 80)
    print("DOWNLOAD SUMMARY")
    print("=" * 80)
    print(f"Total images processed: {total_images}")
    print(f"Successfully downloaded: {successful_downloads}")
    print(f"Failed: {total_images - successful_downloads}")
    print(f"\nInputs saved to: {inputs_dir}")
    print(f"Outputs saved to: {outputs_dir}")
    print("=" * 80)

if __name__ == "__main__":
    main()
