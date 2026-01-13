import json
import math
import urllib.parse
import scrapy
import os, sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pricemate.spiders.spider_lazada import PricemateBaseSpider

cookies_th = {
    '__wpkreporterwid_': '3f95e84c-055b-460c-2335-5deb47fc6bfa',
    'lzd_cid': '08313b6f-3467-4c9a-bc12-874b8e8ea90b',
    'lzd_sid': '113a8d025e5b1608e1776b5edff04e85',
    '_tb_token_': 'e37dbb318b336',
    'lwrid': 'AgGan9c7iva0ja5F%2BLN8X39uI5Qx',
    'hng': 'ID|id|IDR|360',
    'userLanguageML': 'id',
    '_m_h5_tk': '32b15cab76aa02b2b0b06a25bc49d9f8_1763626198222',
    '_m_h5_tk_enc': '427a21107077fbd1549ca4f8464a0d3f',
    'undefined_click_time': '1763618279665',
    '_bl_uid': 'b8mktiCm72n0mdsn5dhFv2ph9tb2',
    't_fv': '1763618282959',
    't_uid': '28Tz7cyoBuK0pD3P7pf7icf0PTFkxVK8',
    't_sid': 'mVwUNY0iOWIP3ebzbOLqUnNIsB0D3Y17',
    'utm_channel': 'NA',
    'lwrtk': 'AAIEaR8ecB1O8YoEFhGMqm7uUCwo4he+yq1kaD+NDCL2l1443FNPZGA=',
    'x5sectag': '408939',
    'bx-cookie-test': '1',
    'x5sec': '7b22617365727665722d6c617a6164613b33223a22617c434e58652b736747454e544f754d514249676c795a574e686348526a614745776e4f484873674e4b616a41324d446c6d5a6a41774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4451324e7a5a6a5a5464694e5759354d3249324f44673059544e695a6d51774e6a4d774d4441774d4441774d4441784d54566c4e7a6b34596a59774d444178596d4d784e325a6a4f5442694d6d5933597a41304d6a67314e47493d222c22733b32223a2261363636313730346163326366653761227d',
    'tfstk': 'fJbWr3Tk-YDSwSt-b6FqfrNZNwTBVTaaVXOds63r9UL-pvC93ePoYuABRK6HUHIzKtMdL13yU6JPhbbfC2uzEufKRe8LQRza7sNk-eeZsbSrDYAkN0Uee4pv2lfiRRza7_ISErS8QglCCDK69edJeLKYGBRHpeKJvrFX9Bk-v4BdMU6LEkh1v-JtRgmECjWa5-3E8ZOYZdC51IAVlttJBnpjJB_XN3TONNnVtRAAuZtw0XPWk1jVeIT_PAA5D1TJOwVtAptCrE9fCP3HigB5kH_4tPC2PBt9JnGKJsTf4ndyWPHXiiCPvaXSO2dlzN-BInNK-H8A7hIOFXVGMUdd4ZuwCo6mAjtiRI9aGSinxvTOfJlyJIOw2IA00SNjjQtJiI9aGSinx3dDi-PbGcA5.',
    'epssw': '11*mmLtDmNIBsz9xima3uAkw39qnCymXcZGW5uEuBjAYg8aX5fg3PKcLvORLbK2qmbxIlYP7stmx6Ji7qAZ3teKyREmaOAmoJPmEl1mKKAZa7EA7rmmEpkPQ2vDmLNRHRmkRuSv7q7ecnHUJSDI5xyvQRAhm-F7njEgeMR7moIEi5PW2WCa9ukYwhN3YdCAiqnNsDrmaimTiWBiiQTEFImmGBE0zGNT1_3mmHWmmoJSqFK71lpC10ulDimmqZge_i-qBmjTfDea0eNeuu0plimmEmNYNjaEfDPYPd8aV9DemCuFBjeLB1Lxom03VNI2mzeTLeamEB..',
}


lazada_cookies = {
"cookies_ph": {
    'lzd_cid': 'd5a38751-98ed-4afb-9da8-e1f79687fa5d',
    'lwrid': 'AgGapVy8%2FQkXtUjELOV2X39uI5Qx',
    'hng': 'PH|en-PH|PHP|608',
    'userLanguageML': 'en',
    '_bl_uid': 'snmakiC28epjbjxtvu9dkRyzb3qn',
    't_fv': '1763710914005',
    't_uid': 'hJmbBibfo7Y5YVxlmPlPpfjzvdO2U9fQ',
    'lzd_sid': '1f9a680504a52044a788963a4faa34a0',
    '_tb_token_': '7d1d0b357f3fb',
    'undefined_click_time': '1764480023901',
    '_m_h5_tk': '94b6c1fe00aac1c5d2185314ea00c718_1764487588831',
    '_m_h5_tk_enc': '16088960a84d15f96bd42d9712dbac9f',
    'lwrtk': 'AAIEaS0ll3/dozHSJKss50C9vkS/qVKgy4HLqh1uMfVu2y3Yk8GK6o0=',
    't_sid': 'u612sFrbSLNHqMg64UupRQFPrIgohiwB',
    'utm_channel': 'NA',
    'isg': 'BGRk0y6u0frfVyU7OcqiZOgjNWJW_Yhnsxp0L36F6C_yKQTzpg5N9YnC7Zkx8cC_',
    'epssw': '11*mmLxzmXhjTCehmmaEN0dkS2BG85sdKUe_f-iSuoTkBUOCWtBJ7qkEc_U3-PFMNkrqaafytEUWZTmRRAxmmECZmAxaOAvQREm3Cmv9UeiOp8Hl-pj3giUCyiOVbjIJdrkzSxHRRBxEMRJaRmim-pM5IyFeWd3meP51QZmar7uBIchLQoS3MVZiqpy09FqPKAEBqboriCLmiEvuRhf5eom1_3mQjpqBAZqqJUFF0uuFun_mmmwuuw_qhPTEBeeECFmuuuu9o2nfDjmmvgaEmHuuYhnBg2-NRBmNjPYsJF58cA6BpFra1ERfLnbucw.',
    'tfstk': 'gdvm5cgSVI5fj62bicXjiSrfXchJct61cFeOWOQZaa77krevbcXMmFvtchuXSdbkbFQ2Xm_NbUThg-QOH1yGzQgjlxMfbdYBNqgjhxTkbHLJD-p9IQwMAh9xcOnfhn61Q23KpFxXcOG9-Yury3oNfOjqY5PvPn61Q4hgLz46cEQkgC6NQ0XPjMrVQs7qq_SGz-Sa3GzrqG_PQ-WNu3zPbGUN0R8w40j1zNWNQFWrqG_P7OWZNrufkt6pUVwMqt3faC9lmsbeqYwaIB2diw8NrRueEi2V8n7uQR7FiThvqn30d3BXKejpkYyD-h-B__vgz2b6E3J2_3am49xkwBCDZqyGyKQROKW3bx-lnZfeUUEqDe-kbBCkeDkCnt726ttTxqKknEKXEhEaatXvZ6vcLvaVWQKHIGvs5YYHbHONZd4c4sPzTiyuCgo9E5N1ggslJp-WhBwy1-SEq0VF8sS5czmoq5N1ggslJ0muTH5VVial.',
    'x5sec': '7b22617365727665722d6c617a6164613b33223a22617c434c6a4b744d6b47454a6d646a34594749676c795a574e686348526a614745776e4f484873674e4b616a41324d446c6d5a6a41774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4451324e7a5a6a5a54646d4f5759354d3249324f4467305a6a6c684f474e6b5a5451774d4441774d4441774d4441784e4441334f544e6d4e7a566a4f5755794d3259784f5745315a6a41354f545933595449354f4451325a54673d222c22733b32223a2237346636383865333063323234653534227d',
},

"headers_ph" : {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.lazada.com.ph//nestle-store//_____tmd_____/punish?x5secdata=xfFQ4l3dAvLc7kmJgyg_98j1WskckIHhOBpMmL-nKrqUlM0_Db_dFkGkSPCRnvJzEvO1F_CMbosS8MU1UV3wM3oEOvsbi8mpN44qqT7Z-1RmhPm0QtdSPPdCnIGnKjK6MQkY_lNcQDhWbNDnJxr1HQmt0QXI1lHoKOSRVy72FfErLMfvo0cwPhRwnjdRRiM_RYMSiZBkauGgBuQft_FwCzMGkZ2UhY9CWqqE4SIn9nPaGVQ_J4Y0fvqaosmQMT4qT9HBuGCQvIXPSi25m2rsION-dDW1YJcjQdQHyih1OF0vlego56KMAg01vASDu-O1EOsvVIflxYTxZI3fHhNWDjKDElZAqThkfC4WHJ3sdG-4VuMQn6soTRzXHfAqLTXOFPdz77_slY2opfn9frEYZguSdfH1QAd_QkZAEPVPBCXBIZ7zKPhEKanayb5GkvDdBQPWaj-8kDsn2YQv4hlQacVqeq4FF5cT_jBJYP1K8NwcQ7eBMBWiqx2wakP98RrLB23K_KWzs4mXm-JblflRhGgdi-MXuBIlsfap3Ur6V9AlnTL0fbwgPEZ6YGR4RZXWIIusM1rbHNCEiUPX1bV4LZqkpIF4LJg_oyJu7e4dB3T4-kZSz0-aQypfhc3uFIdZpdAnrIrspxBZ8kVg7WbaeuDJKHjlgPHMlO8cbTof7flctHdUX2e0S0X86lKSqpf62yjbHjjwrYpxpY53GBcPALgQ__bx__www.lazada.com.ph%2fnestle-store%2f&x5step=1',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': 'lzd_cid=d5a38751-98ed-4afb-9da8-e1f79687fa5d; lwrid=AgGapVy8%2FQkXtUjELOV2X39uI5Qx; hng=PH|en-PH|PHP|608; userLanguageML=en; _bl_uid=snmakiC28epjbjxtvu9dkRyzb3qn; t_fv=1763710914005; t_uid=hJmbBibfo7Y5YVxlmPlPpfjzvdO2U9fQ; lzd_sid=1f9a680504a52044a788963a4faa34a0; _tb_token_=7d1d0b357f3fb; undefined_click_time=1764480023901; _m_h5_tk=94b6c1fe00aac1c5d2185314ea00c718_1764487588831; _m_h5_tk_enc=16088960a84d15f96bd42d9712dbac9f; lwrtk=AAIEaS0ll3/dozHSJKss50C9vkS/qVKgy4HLqh1uMfVu2y3Yk8GK6o0=; t_sid=u612sFrbSLNHqMg64UupRQFPrIgohiwB; utm_channel=NA; isg=BGRk0y6u0frfVyU7OcqiZOgjNWJW_Yhnsxp0L36F6C_yKQTzpg5N9YnC7Zkx8cC_; epssw=11*mmLxzmXhjTCehmmaEN0dkS2BG85sdKUe_f-iSuoTkBUOCWtBJ7qkEc_U3-PFMNkrqaafytEUWZTmRRAxmmECZmAxaOAvQREm3Cmv9UeiOp8Hl-pj3giUCyiOVbjIJdrkzSxHRRBxEMRJaRmim-pM5IyFeWd3meP51QZmar7uBIchLQoS3MVZiqpy09FqPKAEBqboriCLmiEvuRhf5eom1_3mQjpqBAZqqJUFF0uuFun_mmmwuuw_qhPTEBeeECFmuuuu9o2nfDjmmvgaEmHuuYhnBg2-NRBmNjPYsJF58cA6BpFra1ERfLnbucw.; tfstk=gdvm5cgSVI5fj62bicXjiSrfXchJct61cFeOWOQZaa77krevbcXMmFvtchuXSdbkbFQ2Xm_NbUThg-QOH1yGzQgjlxMfbdYBNqgjhxTkbHLJD-p9IQwMAh9xcOnfhn61Q23KpFxXcOG9-Yury3oNfOjqY5PvPn61Q4hgLz46cEQkgC6NQ0XPjMrVQs7qq_SGz-Sa3GzrqG_PQ-WNu3zPbGUN0R8w40j1zNWNQFWrqG_P7OWZNrufkt6pUVwMqt3faC9lmsbeqYwaIB2diw8NrRueEi2V8n7uQR7FiThvqn30d3BXKejpkYyD-h-B__vgz2b6E3J2_3am49xkwBCDZqyGyKQROKW3bx-lnZfeUUEqDe-kbBCkeDkCnt726ttTxqKknEKXEhEaatXvZ6vcLvaVWQKHIGvs5YYHbHONZd4c4sPzTiyuCgo9E5N1ggslJp-WhBwy1-SEq0VF8sS5czmoq5N1ggslJ0muTH5VVial.; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434c6a4b744d6b47454a6d646a34594749676c795a574e686348526a614745776e4f484873674e4b616a41324d446c6d5a6a41774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4451324e7a5a6a5a54646d4f5759354d3249324f4467305a6a6c684f474e6b5a5451774d4441774d4441774d4441784e4441334f544e6d4e7a566a4f5755794d3259784f5745315a6a41354f545933595449354f4451325a54673d222c22733b32223a2237346636383865333063323234653534227d',
},

"cookies_my": {
    '__wpkreporterwid_': '60f5d7b0-9070-4918-17ae-f1d3e76981e6',
    't_fv': '1764323729914',
    't_uid': 'hEQZBLfPlbOS7CLCfRWMKlmObjvnhzwO',
    'lwrid': 'AgGan%2Fc36WmdiDZV%2BOCTX39uI5Qx',
    'hng': 'MY|en-MY|MYR|458',
    'hng.sig': '3PRPmcBmKLS4UwrxxIzxYKE2BjFcClNbRbYGSaUai_0',
    'lzd_cid': 'b15e9aab-add0-403b-8209-41360905fa98',
    '_bl_uid': 'gvm31i5Fi6zrhmf0n5kR28h15Cgs',
    'lzd_sid': '1e4ea5f41231c90cec1b53c0ad7cd58d',
    '_tb_token_': '73e789853eade',
    'undefined_click_time': '1764420064075',
    '_m_h5_tk': 'd79d37527df7421549c70ec2d09bc194_1764483008252',
    '_m_h5_tk_enc': 'c6b1efb47d7b11c3caa60e75a4812b2d',
    'lwrtk': 'AAIEaSxX71tzweE3vTEbAJ6FIi6E9IHkM61LsGisZIl5DQ7rCYzVcD8=',
    't_sid': 'SgaUsVswnxigmGw7DW4MfLBl8Q1lIum7',
    'utm_channel': 'NA',
    'epssw': '11*mmLbRm247sf3hCvg5KbdkaH_ZQiwCo6r5imm_FEe0P72J09IkSDSHhku6nwWabRsthibTcEUbG05kuvOEOckGEAZ3teZaOAVLOAZlkj-dBSgYh283gGgfuvdxw38oqIk-nRKQRBxoL5baOA-gYV5Mxx_eV33meP515PWlo3StYAXbsO3A92cVpcAs9FqGRHF0UX5sDzgmiTqmCrf59cJmmHu2wmm0lVqqCUmF07CZ_Tsmmmwuuw_qhPTuc3eEeEDEmEYX6pEuu7aNBBmBjaEBb3BE5ilJCuuADjeH1AY8cfgE4AM-q2JuOfaBem.',
    'tfstk': 'ggfs5GAMicmsmlWJCIzEFH2tlwAb4yPrXqTArZhZkCdtDmQJYIzi3RYXGHsDbd7A7SICcGswBI52GKIFc1uw65jFY9Bngdr0sMSFp9x90F74GnIM6KXw0h-XGZj78uPzaNbMiBEz475xOiZXinF2MJRKRHx14uPzaNBaSRjQ4OSxIiYDkIL9HnFLRE8DMEpODHppyUo9MIIYRHLJPAnxMfdL9F-pDIdADwUBoHL9MIIAJyTmNYwe8x-15zvmb317KTb9AjhA6Rv6ViMqMjBJ5d1AWH9Xh6T6C3pXoaS56M7A_1v3pvOc8TsfHgEEQhBWPM9PCuG1VGYAlEI_Z4td1Z1BI9uoww9Xf9C9dqhA5N-f4ts_fAxOQM9kJp3bZeSyvNfOdrmdWg-66epUwz_pH95ME1rK1QBl7CWA2kkwXTTA49cyVJsnh29oMetzRyMmnmORFoSsjBhXBeYEPyaIfHp9-etzRyMmndLH87aQRctd.',
    'x5sec': '7b22617365727665722d6c617a6164613b33223a22617c4350364d734d6b47454f4c57344b384549676c795a574e686348526a614745776e4f484873674e4b616a41324d47466d5a6a41774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d44526b4f546378595749784e3259354d3249324f4467304e3245334e32566b4e4745774d4441774d4441774d4441784d7a426d5a474d794d5441324e5451314d57566c5a5759355a6d49795a44517a4e324e695a54566a5a57453d222c22733b32223a2261613933353334623562646130373035227d',
},

"headers_my" :{
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.lazada.com.my//big-pharmacy//_____tmd_____/punish?x5secdata=xf6nhHt0wFzOqoViuB9q9DjiwTuIQ1vXO_BGZUpWxlaQG8vod_nbmlsm0EXQLNyZTGwTjN7_bfHOluG0sqrGLWPkXMx6zr3uXJPBJVxJD4I-1exAXTmg5TC-buhdw0kxcEDTiS38yr0tAoY1x2BWv1T74Arh4ZstSNGFSVwdIwdK6H3I_oaLF4AO8LNxses_vNLYMYtXzZdgXiknrwSdXziDor7T6P9kjpvkTIm7i7Iq-6yI99U75OFeDGG8wshsus5e7FU5IDS1p1hyC-KSFccLgokLuvGUQ-CJNpKdI8uSIubxEGn_iFUsUK5GRGAbDlSt-YXRTZnedkh5NaohS9CgjnbmEKtnXZ6eEMfw9g3DgsXiQEcXF6AVUYjEER6lSUiJNw0wDVoGnIUvelEBmZdDn_vOqfHX88JL-CKp1V08An6Xe-5Fs8XYPhC6flaNZBcnlMjRvgBMW4LEV-ss_5idShctxBcFeJw21pMM5WBz23iF94831Ce3jET6DbWajNyB3XyyU3ndPNGj19-jWx-D0uN4CJoWh9fqNicD_FP19nf_-ZXv4YAIQeMuiEiJzCk6_tYefCVcLpH7AO5y2RTWbKpt3hYzLTonh_rXYTB6PHqiTCMifhbMDAmEK7RfxKOA4-ZtwGYWMxbkUaJgJiAlalK6sGdRUDuMdo-b5DnQwOIxwDMl4_wctMi-hnw2e90o8QP_sFk4FhKVEjIEn2PA__bx__www.lazada.com.my%2fbig-pharmacy%2f&x5step=1',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '__wpkreporterwid_=60f5d7b0-9070-4918-17ae-f1d3e76981e6; t_fv=1764323729914; t_uid=hEQZBLfPlbOS7CLCfRWMKlmObjvnhzwO; lwrid=AgGan%2Fc36WmdiDZV%2BOCTX39uI5Qx; hng=MY|en-MY|MYR|458; hng.sig=3PRPmcBmKLS4UwrxxIzxYKE2BjFcClNbRbYGSaUai_0; lzd_cid=b15e9aab-add0-403b-8209-41360905fa98; _bl_uid=gvm31i5Fi6zrhmf0n5kR28h15Cgs; lzd_sid=1e4ea5f41231c90cec1b53c0ad7cd58d; _tb_token_=73e789853eade; undefined_click_time=1764420064075; _m_h5_tk=d79d37527df7421549c70ec2d09bc194_1764483008252; _m_h5_tk_enc=c6b1efb47d7b11c3caa60e75a4812b2d; lwrtk=AAIEaSxX71tzweE3vTEbAJ6FIi6E9IHkM61LsGisZIl5DQ7rCYzVcD8=; t_sid=SgaUsVswnxigmGw7DW4MfLBl8Q1lIum7; utm_channel=NA; epssw=11*mmLbRm247sf3hCvg5KbdkaH_ZQiwCo6r5imm_FEe0P72J09IkSDSHhku6nwWabRsthibTcEUbG05kuvOEOckGEAZ3teZaOAVLOAZlkj-dBSgYh283gGgfuvdxw38oqIk-nRKQRBxoL5baOA-gYV5Mxx_eV33meP515PWlo3StYAXbsO3A92cVpcAs9FqGRHF0UX5sDzgmiTqmCrf59cJmmHu2wmm0lVqqCUmF07CZ_Tsmmmwuuw_qhPTuc3eEeEDEmEYX6pEuu7aNBBmBjaEBb3BE5ilJCuuADjeH1AY8cfgE4AM-q2JuOfaBem.; tfstk=ggfs5GAMicmsmlWJCIzEFH2tlwAb4yPrXqTArZhZkCdtDmQJYIzi3RYXGHsDbd7A7SICcGswBI52GKIFc1uw65jFY9Bngdr0sMSFp9x90F74GnIM6KXw0h-XGZj78uPzaNbMiBEz475xOiZXinF2MJRKRHx14uPzaNBaSRjQ4OSxIiYDkIL9HnFLRE8DMEpODHppyUo9MIIYRHLJPAnxMfdL9F-pDIdADwUBoHL9MIIAJyTmNYwe8x-15zvmb317KTb9AjhA6Rv6ViMqMjBJ5d1AWH9Xh6T6C3pXoaS56M7A_1v3pvOc8TsfHgEEQhBWPM9PCuG1VGYAlEI_Z4td1Z1BI9uoww9Xf9C9dqhA5N-f4ts_fAxOQM9kJp3bZeSyvNfOdrmdWg-66epUwz_pH95ME1rK1QBl7CWA2kkwXTTA49cyVJsnh29oMetzRyMmnmORFoSsjBhXBeYEPyaIfHp9-etzRyMmndLH87aQRctd.; x5sec=7b22617365727665722d6c617a6164613b33223a22617c4350364d734d6b47454f4c57344b384549676c795a574e686348526a614745776e4f484873674e4b616a41324d47466d5a6a41774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d44526b4f546378595749784e3259354d3249324f4467304e3245334e32566b4e4745774d4441774d4441774d4441784d7a426d5a474d794d5441324e5451314d57566c5a5759355a6d49795a44517a4e324e695a54566a5a57453d222c22733b32223a2261613933353334623562646130373035227d',
},

"cookies_id": {
    '__wpkreporterwid_': '15097f56-8298-4369-19c6-c5209c2c984d',
    'lzd_cid': '08313b6f-3467-4c9a-bc12-874b8e8ea90b',
    'lwrid': 'AgGan9c7iva0ja5F%2BLN8X39uI5Qx',
    'userLanguageML': 'id',
    '_bl_uid': 'b8mktiCm72n0mdsn5dhFv2ph9tb2',
    't_fv': '1763618282959',
    't_uid': '28Tz7cyoBuK0pD3P7pf7icf0PTFkxVK8',
    'hng': 'ID|id-ID|IDR|360',
    'hng.sig': 'to18pG508Hzz7EPB_okhuQu8kDUP3TDmLlnu4IbIOY8',
    '__itrace_wid': '174ffcae-db3d-4ecc-8525-c6728da557ea',
    'isg': 'BODgXucJnQZhUyECfQ2PALVtse6y6cSzn_ZwM1rxrPuOVYB_AvmUQ7Ym7eVVZXyL',
    'cna': '7t2tIbdZvkoCAQ5ga4vT0Oef',
    'lzd_sid': '13df68fc13b409cfe984233185077e85',
    '_tb_token_': 'e33e8e6ee19be',
    'undefined_click_time': '1764476127068',
    'lwrtk': 'AAIEaSw1Xp7SwQwrmxdoVQA/D/UI2VEpNMFRMxAjuR5M1fQZ0Xxf1j8=',
    '_m_h5_tk': '183c9cc0279db0dabfd5bfd64685f48f_1764484412463',
    '_m_h5_tk_enc': '501d59317e4771b5ed12a4a4875b90c0',
    'x5sec': '7b22617365727665722d6c617a6164613b33223a22617c43494b6872386b47454957386a3944372f2f2f2f2f77456943584a6c5932467764474e6f5954436334636579413070714d44597759575a6d4d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774e4749304f54566c4e44566a5a6a6b7a596a59344f4452684d324a6d5a4441324d7a41774d4441774d4441774d4445774e6a51324e6a4e6a4e6a4d7a4e6a4d304e6a49774e57557a5a5759304e6a56684e4445344d6d51304e413d3d222c22733b32223a2265313962316462333063343532613165227d',
    'epssw': '11*mmL-ZmqVpsG_gCvgBomk4hxJ2ADzK7MEwiKyaRIvEmzbsXwcODMWQe2rRw-sFOFWGfo-QTE1KbLWpbt-3teSiNAZaOAZaRHTE4yQ-3diOp2S3GCb3g48q2h5P60YvlIk-nzHdOAZarf-xtVMBaDgmDImNdEm1A0dInW7JS5NaJAei7rmF2zwzyptZucnKFagiaXmB1jijJFfqKJx2R5U27UpGBH3-1NTme7CmHLmmoWJ2vlnl0ucu0u0kmmmqjam5H2s8tFufDeaYCF0uu0plimmuuyemmBmBjaEjxn02fLYNjaaBjvryRjyom03VS4G5eERdZgefR..',
    'tfstk': 'f0dsTefGilq_mK6TUE3UFTDt2OCbhhGykr_vrEFak1CTDoLRYsug3AbfGMtcbtpZmH6X4nwagRRVGSKhAFWqm1JbGEKsSGdXoS_vkn0G0VDeSFfcM0oXcb8MSr24lJoFMqLLy2gKgblySFEUXT9tadoCa-BPDsBOXMBdxNaTHnBTpkIhoZEOk53BJUmStqeKvFrzOWeujoHHmj1U1BQ1CiwNASwjuN612FII20dIGOsJW6NjXKD8oisHwDkB-EJ9bwxjND1JEHOfesG_qN9pP6INwYwC1e-MN1dSf57FTGWJH9gt6e11ftQGFjoG1KKMGOv_o4Yd6HvlqOHnxwOwatsldkn98esOFKszJ7SSdH2bRTVfRguIR-20c_pS0P5ARaWO-wzSR2Z1vOQhRguIR-2cBwbEN2gQfMC..',
},

"headers_id": {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'referer': 'https://www.lazada.co.id//beautyhaul-indonesia//_____tmd_____/punish?x5secdata=xfgT1OsCIIq6Gbq2NmP3eL2i_wu32K-af_QtfzadqJJBejEqV6-pL9wNIM_2A3FGij3Z-v5LBpABjCz67gfvBL3KPWU19uNGz-yaDI1sI_gBFqw5qtc-FWDNhYRZrddYCjDZmMQcpyhDNF8E33umk05ItI3QuJEDot6hNKtbYewlSNt7Xf5JE42FeoEEH2b7v3VxRoG3hdTwoDiNkqQhXDoJgJjbYnwJWFlyJ1-eEO1okew4XikdN-GpIthmfJgUkzmjM57Da_MO3Ro5R77kCypaWBXAvksD9VFEX2g-8A8rPBOyVnxdQQCpmr6Z5IdUxhdpE4x2AXsGUQz2lwlArmzSd4o1WzgiCJnQtJ2kEca6MpXJqqMFIsgA2LzJyZC0l9X71axQHMqzNC4k-JZEAGQZNEEawNOUCYdGHGL1ssbKxsH78mORU9x2cfOFWZ66eUB8ssHBcECO7ommnrR3EbSW3A5EDQ6lra_ImsaG5xnOiink6MVU6ZjjiN2LqSVo_gfOxpvK8D80AYU-HWuU1yGyErhosUo9x6oHeo1OpsZhYVIKx6U7vDtBfHDlVgWNYDugCVPjOTotetKgNszvFg7cwbNojEFlRkfeAwV9vIaQc2usCYq2rjxqTu8S6-MhySV7M-Nj8A1P-Uy0_z4X2M98DeMj3ekZQkusblhpwmE31WXpvkl0XMuJMgwyhknhbuISXQnusGKlnc71P235MG7A__bx__www.lazada.co.id%2fbeautyhaul-indonesia%2f&x5step=1',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    # 'cookie': '__wpkreporterwid_=15097f56-8298-4369-19c6-c5209c2c984d; lzd_cid=08313b6f-3467-4c9a-bc12-874b8e8ea90b; lwrid=AgGan9c7iva0ja5F%2BLN8X39uI5Qx; userLanguageML=id; _bl_uid=b8mktiCm72n0mdsn5dhFv2ph9tb2; t_fv=1763618282959; t_uid=28Tz7cyoBuK0pD3P7pf7icf0PTFkxVK8; hng=ID|id-ID|IDR|360; hng.sig=to18pG508Hzz7EPB_okhuQu8kDUP3TDmLlnu4IbIOY8; __itrace_wid=174ffcae-db3d-4ecc-8525-c6728da557ea; isg=BODgXucJnQZhUyECfQ2PALVtse6y6cSzn_ZwM1rxrPuOVYB_AvmUQ7Ym7eVVZXyL; cna=7t2tIbdZvkoCAQ5ga4vT0Oef; lzd_sid=13df68fc13b409cfe984233185077e85; _tb_token_=e33e8e6ee19be; undefined_click_time=1764476127068; lwrtk=AAIEaSw1Xp7SwQwrmxdoVQA/D/UI2VEpNMFRMxAjuR5M1fQZ0Xxf1j8=; _m_h5_tk=183c9cc0279db0dabfd5bfd64685f48f_1764484412463; _m_h5_tk_enc=501d59317e4771b5ed12a4a4875b90c0; x5sec=7b22617365727665722d6c617a6164613b33223a22617c43494b6872386b47454957386a3944372f2f2f2f2f77456943584a6c5932467764474e6f5954436334636579413070714d44597759575a6d4d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774e4749304f54566c4e44566a5a6a6b7a596a59344f4452684d324a6d5a4441324d7a41774d4441774d4441774d4445774e6a51324e6a4e6a4e6a4d7a4e6a4d304e6a49774e57557a5a5759304e6a56684e4445344d6d51304e413d3d222c22733b32223a2265313962316462333063343532613165227d; epssw=11*mmL-ZmqVpsG_gCvgBomk4hxJ2ADzK7MEwiKyaRIvEmzbsXwcODMWQe2rRw-sFOFWGfo-QTE1KbLWpbt-3teSiNAZaOAZaRHTE4yQ-3diOp2S3GCb3g48q2h5P60YvlIk-nzHdOAZarf-xtVMBaDgmDImNdEm1A0dInW7JS5NaJAei7rmF2zwzyptZucnKFagiaXmB1jijJFfqKJx2R5U27UpGBH3-1NTme7CmHLmmoWJ2vlnl0ucu0u0kmmmqjam5H2s8tFufDeaYCF0uu0plimmuuyemmBmBjaEjxn02fLYNjaaBjvryRjyom03VS4G5eERdZgefR..; tfstk=f0dsTefGilq_mK6TUE3UFTDt2OCbhhGykr_vrEFak1CTDoLRYsug3AbfGMtcbtpZmH6X4nwagRRVGSKhAFWqm1JbGEKsSGdXoS_vkn0G0VDeSFfcM0oXcb8MSr24lJoFMqLLy2gKgblySFEUXT9tadoCa-BPDsBOXMBdxNaTHnBTpkIhoZEOk53BJUmStqeKvFrzOWeujoHHmj1U1BQ1CiwNASwjuN612FII20dIGOsJW6NjXKD8oisHwDkB-EJ9bwxjND1JEHOfesG_qN9pP6INwYwC1e-MN1dSf57FTGWJH9gt6e11ftQGFjoG1KKMGOv_o4Yd6HvlqOHnxwOwatsldkn98esOFKszJ7SSdH2bRTVfRguIR-20c_pS0P5ARaWO-wzSR2Z1vOQhRguIR-2cBwbEN2gQfMC..',
},

"cookies_th": {
    '__wpkreporterwid_': 'fa0af252-c6aa-43de-a9ad-ca7b8677e551',
    'lzd_cid': 'e0b16b1f-193a-4f86-bc2a-d8f2284418a2',
    'lwrid': 'AgGaoAn5MPOVmPOuO9EAX39uI5Qx',
    'hng': 'TH|en|THB|764',
    'userLanguageML': 'en',
    '_bl_uid': '02m1bibh7Os2X6raXkICl6jjyb80',
    't_fv': '1763621604412',
    't_uid': 'SgUS5yBEvRLf4yAbh2xnqRK1zP7lyp4i',
    'lzd_sid': '10f277f4895901f9b35aa8820ca9c389',
    '_tb_token_': '581d770a3e1e0',
    'undefined_click_time': '1763979403249',
    '_m_h5_tk': 'ffe51d1eeb9dbecc2462fc90f18d4c2e_1763987684623',
    '_m_h5_tk_enc': '7fb8c8daf6a7090712daf65b70f05329',
    't_sid': 'oSPO5UHeAip5olioZRqVtIspPqOGFPAV',
    'utm_channel': 'NA',
    'lwrtk': 'AAIEaSShCxJ+gCTss3d2zymcys6lQIcY08++3drCjYf7DQ1sM4AQgxM=',
    '_gcl_au': '1.1.1478173761.1763979408',
    'cna': 'jx6rIVrHIEICAS2FBAlhwUb1',
    'xlly_s': '1',
    '_ga': 'GA1.3.2106285800.1763979416',
    '_gid': 'GA1.3.884407879.1763979416',
    '_uetsid': 'b45865c0c91e11f08aaa6140e313837b',
    '_uetvid': 'b4588750c91e11f0b0ca771ad45d0821',
    '_fbp': 'fb.2.1763979416335.243092643799194723',
    'cto_bundle': 'vvXIDV9XblY0eUNUeVhMRnZWc29KSnMyJTJCaUV0YWlCOThHVFp4SFE5Z0YycFpRJTJCdm1uSTg2NHYzSE4wRGxSVEpLbSUyQkdrT2RHOTlUdHEyRUIyOWUlMkZGMmtpNTdEZnU3JTJGcjVDRlNGeFdZbEpXVm5TWldPQms3byUyQkQyYVc2c0txMURrd1VVZGpmMzlIT1olMkZOQmpvVm0xUmpMWkMlMkJRZ0gxSEtXSDZLZW5nUUQzMTc4cHBVJTNE',
    'AMCVS_126E248D54200F960A4C98C6%40AdobeOrg': '1',
    'AMCV_126E248D54200F960A4C98C6%40AdobeOrg': '-1124106680%7CMCIDTS%7C20417%7CMCMID%7C34947093032700580204267579038899530150%7CMCAAMLH-1764584218%7C8%7CMCAAMB-1764584218%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1763986618s%7CNONE%7CvVersion%7C5.2.0',
    'isg': 'BFVVgtYMkLBzGrTMdz24J0XPZFEPUglkKj2FPNf6UUxiLnQgn6J4NBHv_CqYLiEc',
    'x5sectag': '204372',
    'x5sec': '7b22617365727665722d6c617a6164613b33223a22617c434c44686b4d6b47454b79506d5044392f2f2f2f2f77456943584a6c5932467764474e6f5954442f797065612b502f2f2f2f3842536d6f774e6a41355a6d59774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441304d6d51344e5441304d6d526d4f544e694e6a67344e44566d596d59314e4449334d4441774d4441774d4441774d575133595455315a5455344d4452684d6a55324e7a646c5a6a5a6c4d6a597a5a4751344d6d55334d544e6a222c22733b32223a2262333066373962336230643035366432227d',
    '_ga_HKW7PMMCHF': 'GS2.3.s1763979417$o1$g1$t1763979471$j6$l0$h0',
    'epssw': '11*mmL4UmC62TzjgmmaEN0dcWdBwpKOPgKYFyFo9McNrxnO5M4jeRoy7Gq0G7x33gYlASaRdihEkyyOxtZK3tvMSuvOaOAmmCHKE4yms1BhOw89KCPpEVJPpNv42cXZDlIkhsGHRuvOEOM-xg0rBaDs1zkCSiQmKZPQcRz3gsx3U3BPmW0u5paWzypq1ccn8MvO7V4wGiTYGsbG1_uuuryU1_MWbFK71lFuuRNmkBmmqjam_i-pumjEfDaVrZfaBjQqAd8aBjPYNjaEfDPEBBmmV58EBtuFfDP9H1Lxom3KLTKqAZsJn-geBm..',
    'tfstk': 'gADSUj2uKab5cClTNJ-V1oh4CDyIdnJZ9MZKjDBPv8eRJwnTuJ-lTQqQdrg3zWUELqaKrq4UyQxoRXiiy3mr8QcQA8Dqa9zyrJiK7JTw7dJZq020pF8whNs80JEpLyd4wr8aIKLw7dJV-NYubFoyRJeSDk4Y2kB8vnaYbrC8v2U8MZE_xJUKJ2eYkkqLJ6U8yZBYokeLJ2epcmU0AJUKJJKjDbhGfoB0l0tifzbxehKKVr6dpxZvqPn7koqmhuF7WSUfp0MbV7at2ACqWEZx3xNagM84Hccqyow6FNqSMcw8AvxOOyNIE-aj5dB3mb3SHWM2xdn4FkNTpSsdpmwjaSEzBdQbmjnr9Y05A9EoUAPQSStdKWyxQ5htPMxiD8EK-5DeST4-vcDi_R95SuGxf-sP_Oz6GqfCc5XLcP-Xc6fhRRh68PMh0MF8moA2cn1gV7E0cP-Xc6f3woqDuntfsu1..',
},

"headers_th" : {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'x-locale': 'en_TH',
    'priority': 'u=1, i',
    'referer': 'https://www.lazada.co.th/',
    'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    'x-csrf-token': '581d770a3e1e0',
    # 'cookie': '__wpkreporterwid_=fa0af252-c6aa-43de-a9ad-ca7b8677e551; lzd_cid=e0b16b1f-193a-4f86-bc2a-d8f2284418a2; lwrid=AgGaoAn5MPOVmPOuO9EAX39uI5Qx; hng=TH|en|THB|764; userLanguageML=en; _bl_uid=02m1bibh7Os2X6raXkICl6jjyb80; t_fv=1763621604412; t_uid=SgUS5yBEvRLf4yAbh2xnqRK1zP7lyp4i; lzd_sid=10f277f4895901f9b35aa8820ca9c389; _tb_token_=581d770a3e1e0; undefined_click_time=1763979403249; _m_h5_tk=ffe51d1eeb9dbecc2462fc90f18d4c2e_1763987684623; _m_h5_tk_enc=7fb8c8daf6a7090712daf65b70f05329; t_sid=oSPO5UHeAip5olioZRqVtIspPqOGFPAV; utm_channel=NA; lwrtk=AAIEaSShCxJ+gCTss3d2zymcys6lQIcY08++3drCjYf7DQ1sM4AQgxM=; _gcl_au=1.1.1478173761.1763979408; cna=jx6rIVrHIEICAS2FBAlhwUb1; xlly_s=1; _ga=GA1.3.2106285800.1763979416; _gid=GA1.3.884407879.1763979416; _uetsid=b45865c0c91e11f08aaa6140e313837b; _uetvid=b4588750c91e11f0b0ca771ad45d0821; _fbp=fb.2.1763979416335.243092643799194723; cto_bundle=vvXIDV9XblY0eUNUeVhMRnZWc29KSnMyJTJCaUV0YWlCOThHVFp4SFE5Z0YycFpRJTJCdm1uSTg2NHYzSE4wRGxSVEpLbSUyQkdrT2RHOTlUdHEyRUIyOWUlMkZGMmtpNTdEZnU3JTJGcjVDRlNGeFdZbEpXVm5TWldPQms3byUyQkQyYVc2c0txMURrd1VVZGpmMzlIT1olMkZOQmpvVm0xUmpMWkMlMkJRZ0gxSEtXSDZLZW5nUUQzMTc4cHBVJTNE; AMCVS_126E248D54200F960A4C98C6%40AdobeOrg=1; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C20417%7CMCMID%7C34947093032700580204267579038899530150%7CMCAAMLH-1764584218%7C8%7CMCAAMB-1764584218%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1763986618s%7CNONE%7CvVersion%7C5.2.0; isg=BFVVgtYMkLBzGrTMdz24J0XPZFEPUglkKj2FPNf6UUxiLnQgn6J4NBHv_CqYLiEc; x5sectag=204372; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434c44686b4d6b47454b79506d5044392f2f2f2f2f77456943584a6c5932467764474e6f5954442f797065612b502f2f2f2f3842536d6f774e6a41355a6d59774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441304d6d51344e5441304d6d526d4f544e694e6a67344e44566d596d59314e4449334d4441774d4441774d4441774d575133595455315a5455344d4452684d6a55324e7a646c5a6a5a6c4d6a597a5a4751344d6d55334d544e6a222c22733b32223a2262333066373962336230643035366432227d; _ga_HKW7PMMCHF=GS2.3.s1763979417$o1$g1$t1763979471$j6$l0$h0; epssw=11*mmL4UmC62TzjgmmaEN0dcWdBwpKOPgKYFyFo9McNrxnO5M4jeRoy7Gq0G7x33gYlASaRdihEkyyOxtZK3tvMSuvOaOAmmCHKE4yms1BhOw89KCPpEVJPpNv42cXZDlIkhsGHRuvOEOM-xg0rBaDs1zkCSiQmKZPQcRz3gsx3U3BPmW0u5paWzypq1ccn8MvO7V4wGiTYGsbG1_uuuryU1_MWbFK71lFuuRNmkBmmqjam_i-pumjEfDaVrZfaBjQqAd8aBjPYNjaEfDPEBBmmV58EBtuFfDP9H1Lxom3KLTKqAZsJn-geBm..; tfstk=gADSUj2uKab5cClTNJ-V1oh4CDyIdnJZ9MZKjDBPv8eRJwnTuJ-lTQqQdrg3zWUELqaKrq4UyQxoRXiiy3mr8QcQA8Dqa9zyrJiK7JTw7dJZq020pF8whNs80JEpLyd4wr8aIKLw7dJV-NYubFoyRJeSDk4Y2kB8vnaYbrC8v2U8MZE_xJUKJ2eYkkqLJ6U8yZBYokeLJ2epcmU0AJUKJJKjDbhGfoB0l0tifzbxehKKVr6dpxZvqPn7koqmhuF7WSUfp0MbV7at2ACqWEZx3xNagM84Hccqyow6FNqSMcw8AvxOOyNIE-aj5dB3mb3SHWM2xdn4FkNTpSsdpmwjaSEzBdQbmjnr9Y05A9EoUAPQSStdKWyxQ5htPMxiD8EK-5DeST4-vcDi_R95SuGxf-sP_Oz6GqfCc5XLcP-Xc6fhRRh68PMh0MF8moA2cn1gV7E0cP-Xc6f3woqDuntfsu1..',
},

}

# lazada_cookies = {
#     "ID": "__wpkreporterwid_=da47c640-2b80-4771-307b-9dada1eb860e; t_fv=1746183646149; t_uid=Z8sVqNq6eXt0mRr8eCJjWOMra5IzpGKU; userLanguageML=id; lwrid=AgGWkKftMuvVhb2LuEIHX39uI4bN; cna=4pObILEpUwMCAS2E4TUQYHhr; lzd_cid=db2ee2bc-6512-45fa-a115-5d92652eb117; hng=ID|id-ID|IDR|360; hng.sig=to18pG508Hzz7EPB_okhuQu8kDUP3TDmLlnu4IbIOY8; lwrtk=AAIEaC3y8+fVmvBlOHqtu3qrJi3s4a22a18gan/pVlL/Ya242IFvj8M=; _bl_uid=5nmj0aIpxz9m28qtz2Fg1jU6p8L1; _gcl_au=1.1.1721755666.1747812985; _ga=GA1.3.2077326855.1747812985; _gid=GA1.3.1405467420.1747812985; _fbp=fb.2.1747812985176.816970357211560397; AMCV_126E248D54200F960A4C98C6%40AdobeOrg=-1124106680%7CMCIDTS%7C20230%7CMCMID%7C89957873523627905782470703107115927170%7CMCAAMLH-1748417785%7C12%7CMCAAMB-1748417785%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1747820185s%7CNONE%7CvVersion%7C5.2.0; lzd_sid=1fa20132c69e0df653696c06339d9043; _tb_token_=fe5356b17345e; EGG_SESS=S_Gs1wHo9OvRHCMp98md7DG4woCU4KtwaLcBBCsrYJvcQHYHWEwn1yt_VXSyxaTs8QaPWUvZr4Wd3N3WOrwS_HHkvStVbmRCU1Z5sYH7Y1kcO1SYGwm5n0uyv_UbBdnHQYIk_wHemtAA2hDjOx_LgFqAx0E_sIeQc1hI4caaSPY=; t_sid=ugBEeupIEUJErU6OMOiOmPyIVpAbHht5; utm_channel=NA; _m_h5_tk=b3812b5013478187eb394806ac7ebe74_1747834361012; _m_h5_tk_enc=ba7f39ada063c85220f6f04c1f4e3f3c; xlly_s=1; _ga_44FMGEPY40=GS2.3.s1747826448$o3$g1$t1747827074$j60$l0$h0$dLYymUF4IL08a5mABeCZWIYIp5tN7LsuRvQ; _uetsid=64bbbde0362011f09b0b79786502b308; _uetvid=64bbe530362011f09929e7a1025861d8; isg=BGtrLeEzh59QG9tLT2DkNK-B-o9VgH8CXI3AX93pfaoBfIveZFRoUgCX1qQS3Nf6; epssw=9*mmCrPmjsiNxE9AV33AjYZR33jGA70tvput8iniimJXT_gSP8mDHT2uBwut_mmQa4dSDm92HzzL0EmHGLA7zn0M0xsn6pmeTSBppC5MdmItIuVAyIHtV3MBgKalwITZpcwXnIRfbmK4qP9M1t0ucnOszgvLiOVAcJ0uu0GmGdotuuuuuu8r2pUj1ctR8HBqP8FKRbQXdL9ZH4un7hgcSyMTJyjuK36xoAGpYadYA74uhmmmmmmAz7d2qAlARC7mc6nSAGbjp-3VHuNeRG5NIHgiKNoRAEnEYs73s0jbUWofxKvAGNpR8SeLjf7LN2uKHfpss8Ldoz; tfstk=gsGxeCDEW3x0xIcYrqJlIo9yL_TlBL02emuCslqcC0n-R2S0Ccv2C5nEXRG0iVOTWugZjoVgGRitocFghnJqBCn84cewulq_Xc0snUAHtqu4_lN9xBAnAydUtjE1j5N4NRaRZqRHtquXO6oCCBciwB67qlN_ho1SPuzTf1wsf8177u1b5sa_VUEzVPafG5_5FPUdhZi_1UF74PN_fcwXy4Gr8hE5llftLU-pZp-Gh6CKwreYXtq56Dllt-ECfu511oUTH93b21ssNAFJ6KqXLaqaioubkcRFgSwtCjVSG3O_Ovo-6JNpIEyjWYnaibT1hkMmmRl4ei6bJSEYdjwA-_uzCYh8ijtNL408cJFoEL-0ISnxLkyXU3otyomsM8svqlDnrjw-A3f-bRHsi7GXVBIrZXcdGZs3vPXXyUBNQ-ayhzzlLWagT548xEdOQOyyzzEHyUBNQ-azykYvWOWaUU5..",  # Indonesia
#     "MY": "t_fv=1728022200682; t_uid=95svVfxS8eWqhTsVopOVWkO3DUv85OXH; cna=t3SGH6HZGXECAVXLFWAsmIRD; _lang=en_MY; lwrid=AgGWkKfLZHx%2Bn89fFKdyX39uI4bN; lzd_cid=97a60ede-3c1c-46a4-beef-75259aeb6f24; isg=BAIC-Vb53slUssz--jMBNB8UUwhk0wbtIFd0eUwbMXUgn6IZNGPV_BKUT4Pjz36F; t_sid=Sp9Mp34LQsCSs1Fey4WQJmw60eM7cdTe; utm_channel=NA; lwrtk=AAIEaC4nz00WWadaLyonVhW59i1WLDjuWcjNPB9/NsDbrCwVvpYzJB0=; epssw=9*mmCyDmotgHxdWtvRdSsURpqiR354gSa4ut-7i5VJmmF3MImmdSvO3tV74ITP8CKqTKM4Qf7TVADGjCkFg1dR9gxr1V1xYuunRcommHmaVcMM0gfJQN0tpzHcCo5Tvj34VaDrtcuK9Jke7tihRmHmm5__utyR95VST0R4uV3emA3Z_2Sy6NIm3BpVhgnO5sNDdw60XOKuFnegtCxSCgMAmqtBvFMaidmmmmEHdYAR3Az33AL3TIFud2L7hV8W3g53J_4mosejmtsJVc2kwqhu_rYZafbHpPrjlsySrThygqdbBKuQHXbF18kTGaaGBi..; tfstk=g2tj409h5SVbLYjTCZDPdwWwimjsTYoEDR69KdE4BiIY65pdaGk07qX1f_OGgZJ93cdWZCwZnf0DV596Zn8V7Er16_LoijmmmOK6tUcmimmDNdpeaKr2bhTufpvM0xjZnivcjGhETDR6nKjgO5Hm4bJ-BOj1HbSg8MpcjGhr5kF7sKAcN7EDMGH52O6a6GQAMY_RQ_EABoBTwY1lwoEOWNE8yOWhHldOXY9RZOIOHCQxFLhSRJ6slsvjnOlebAwAnKC7XlKxoZ1CpPrTXG6flhpANN_6Vt_f9NBXOxxvadK2ma08PGvyRCT99bzVMe6BNw8jOoOBiOp1BIi3d_KXC3_DzJqpFN1XynQ7Blpfq1Qe5IGbosL2NwXRyRihUB5JnnLSI7pvTssAeaoKdLQ9znbH0bEfvevV0FdKar5vROIy-k5Bu3a_FwqOF6kSFP4iF6kzqjhH2gbAEt_rFYNvSZBlF6kSFP4GkTXfaYM7MFf..; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434d767574734547454e5330717150352f2f2f2f2f77456943584a6c5932467764474e6f5954442f797065612b502f2f2f2f3842536d6f774e6a42685a6d59774d4441774d4441774d4441774d4441774d4467774d4441774d4441774d4441774d4441774d4445774d4441304d6d51344e4755784f5464684e5445354f444e6c4f54646a4f5459334e5442684d4441774d4441774d4441774d57566c5a6a6b78596d513259324e694d544a69595745325a5441304e545a6a4f574d334e7a68695a6a4978222c22733b32223a2231656332373333613338333134663037227d; hng=MY|en-MY|MYR|458; hng.sig=3PRPmcBmKLS4UwrxxIzxYKE2BjFcClNbRbYGSaUai_0",  # Malaysia
#     "PH": '__wpkreporterwid_=e51a2f67-be4b-499e-3ad7-454b42bd425e; lzd_cid=d5a38751-98ed-4afb-9da8-e1f79687fa5d; lzd_sid=1fb2fb588228f03174fd980b44f31df2; _tb_token_=e3e51f11be8eb; lwrid=AgGapVy8%2FQkXtUjELOV2X39uI5Qx; hng=PH|en-PH|PHP|608; userLanguageML=en; undefined_click_time=1763710912099; _bl_uid=snmakiC28epjbjxtvu9dkRyzb3qn; lwrtk=AAIEaSCIQGpad+aKsD5Sns4KBpqoBVfBDh3HHQo84j3AF8Ti3O08jq8=; t_fv=1763710914005; t_uid=hJmbBibfo7Y5YVxlmPlPpfjzvdO2U9fQ; t_sid=E4oed6Jnaz4H4uXgd0pegx4oVo0YTK9O; utm_channel=NA; _m_h5_tk=67668e860e6aab94eab85c77ea5005fe_1763720273186; _m_h5_tk_enc=ba1e7b73624041f7d849659896793ad0; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434d5376674d6b47454f766371344d4649676c795a574e686348526a614745776c4f653476775a4b616a41324d446c6d5a6a41774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4451354d6a51324d4755784f4759354d3249324f4467305a6a6c684f474e6b5a5451774d4441774d4441774d4441784d7a59354e7a67314e5749314e544e6a4e474d784f545978597a51784f5441314e4745774d6a466a4e32513d222c22733b32223a2237336530316631383336363233663762227d; isg=BGJi3D-if51UCGPBy9S8vvrVs-jEs2bN4Ywydaz7vlWAfwP5lEMf3Uy0r6OD795l; epssw=11*mmLtSmBdsXb_ARmaBoElqw7x1jkRuPeSzpYgKtc7jOZ_IzCVnL9hedfAMOiBVKrxvTTLkTE1k9O5V2AZEOkfW4AVEOymoHnEnJei8mdxaw_vvBdxwJP1Q2vDsNl0QifrEoCbJkCA8pJUJSDI5Ncz3rABflimoTTixt_UZeisL1_mNjK9KZTGvRoJOS_Ddikpqnut27Oo2mHCzucng70qKeFUucpvmvFq8OCuuRmm9ImmiM1YcZV0ZimmEeTKmmmnEmQi1C-3BeLENtw744KYNZhWmC7EBZLauu3emmBmg6ME2f_muuuF0uurcyKkdPDQ-coXPVE_oTEmBB..; tfstk=go9sVX6GnP4sGFOR1toUNDNjlUBXCDkPWosvqneaDOBTkrKR8toggfjfhwTc71-A3oTBDFQNuOQZhmT9l1ew7CRflE-2_1QNuE1vzOCD_Z7NlttDPDurUY-MjtXKz4kzzAYkDTjTM5UVpWIlhGK0ES-pjtXx82uGl_xM7ZHfWtBxA9IfVrBAWGnCvG7LBieODwnCmwBYBRQOJwIADPFY6EKKAibdktBvk9nCmwQAHthJYusLKwtsqU6czBr7AU7QH-pCvcbJf6shYps11aCdR-IXdG11yhp8kuqcvpJCa6rq89KkTFICFAalfBK5Bi9m2S_fGdXCRUM8nMA95pCXLmDJYOsfwtCQD-KCdC5dbTH8RMApbIpM5owAjdJPGafID-fVpL5JwFZmqHBODEfk342GWnKkEQWSCzj6936C49wPPXT3Gk1uHM_rADN0ir6JNq81F8z56MjnTDiQZG1OxM_rADN0i1Ihx2oIA7j1',
#     "SG": "t_fv=1746183642299; t_uid=dDeiPkkZizYWTDD4ZXrLYizvL9AYAg59; __itrace_wid=c1e432a4-f03a-4eb4-3ada-3c954fa707cf; hng=SG|en-SG|SGD|702; userLanguageML=en; lwrid=AgGWkKfg%2BO6zPwBFuaDRX39uI4bN; lzd_cid=2bd3007e-814c-408f-9f5e-911133da72e5; cna=35ObIOiWnWUCAS2E4SyVD3hZ; lwrtk=AAIEaC4pOXtFQwvX4a1A5YFfFVCS+/haPiMuzU5834FyvWkoChsH+Uk=; isg=BDMz5DePX_fJkhMacN-0i9XvwjddaMcqJOWIt-XQmNKJ5FKGbTmNeL8_mgwKxB8i; epssw=9*mmCRtmq-eIu_WITm3ts6kC0yQIL70Sa4dSjm_Ho1dSPiaImmdSv7uImm4ITP8mfJM5omQ3CTVA6g-8pzXhiR9ghzAwdkFIHHRcommAuUVcU25lEwH02LcA0ngPc4cUqPVaDNKLm_Vjcev5Mc0uyO9tpFeNvuu_HvL5I4fEZutu3Z_yfHtluc36q9a4fU5ss1vo60XOKu6GM27hOtWnOdmqtBvT1xdSmmmoBEimaXdcLOqsRUWPCS3AH6huLR0ioALuFz7mx9rXNm3_c_CtLdmIoWCCsJchW44bcRzw3g2W0W9UL7tWhd_u_OtwO1wpaHWeMmn0z3Mm..; tfstk=gXXnxPNfO6RI3AU96O9Qi0niSTFOAp9W2aHJyLLz_F8sJ2Hd4uvlxaX8Ag8KrNjloTdLOQKPS15_RywByTxl_1aQRJ9F4Y7G-vQREgMk4g77AUEQ6MsBFLzYka2AAMNLXdwVKUuwbGtmT4P9T2ztHiUYk-eO9mPUhrQRYx54S3TwY3REUlvw4F-yYa8e_V-DcLJPzQlZ_3KxTbRyTRrMVF8yUL7PblxJ7Ul78Y8cUO6a52Zi5tb14OxHtESgCYkl9xdeuNTZUrWMxv8VYFDrUEYgbDsGvyDfXp6conQLQvbc4i1ysT0aoU6Gb95Pf2qwnGfOMBfg8YYOpFdfLKmzLGvH-IWwODDCuGjPMCXT0-9HLe5Jdgn0JGXhJM6G20lwKpCMi9v4h28R6iXkqTa7IZjPc_RGE2jPRflqfekWbuBiNbOefhYvTLfqpqg8ByZgjjNBThtLklqiNbOefhYYjlcjRB-6vrC..; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434c627874734547454f625a2b7233352f2f2f2f2f77456943584a6c5932467764474e6f5954442f797065612b502f2f2f2f3842536d6f774e6a42685a6d59774d4441774d4441774d4441304d4441774d4441774d4441774d4441774d4441774d4441774d4445774d4441304d6d51344e4755784f4756684e5445354f444e6c4f575978597a45315a6d45774d4441774d4441774d4441774d5745314e6a686d4e5749794e6a517a597a526c5a474a6c596a4a6c4d4442694e475a6d4e44597a4e6d526c222c22733b32223a2237653031646137616362303365353039227d; t_sid=c4A3Ksxx1X4iZwIaPg3wMwE2pessIrGJ; utm_channel=NA; lzd_sid=18e7366d9ed4e94d6bfbe04c80b92b48; _tb_token_=35e6ee3103f7e; _m_h5_tk=24bce6a4c3e67f87953b30b11e84d897_1747835523114; _m_h5_tk_enc=ae6431211e66a419e16d56bf81d34ae2",  # Singapore
#     'TH': "__wpkreporterwid_=70c9ec64-4d62-4705-0a1b-dd5b90f9b009; t_fv=1762163546246; t_uid=NqQ5VvW3DCGzsTfyk2uwCGt3YwQByQJe; t_sid=9tTGN9XLK20sz1XFVLGeXgp4pUng5VZD; utm_channel=NA; hng=PH|en-PH|PHP|608; userLanguageML=en; lwrid=AgGaSSHZYMTRWBZ25du6X39uI8qS; lzd_sid=15c29a2ad38f6bbb1e2b68b79b2a0142; cna=WWmPIUbp1kQCAbacblaHOafl; lzd_cid=fa3e4b46-11f1-49c7-95ba-6a770f36f363; _tb_token_=b417938eb0ea; lwrtk=AAIEaQjr3owRBC9JoREPz4LXc7Wf8hBnfHDwivh1No/7/vBh4exo800=; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434e6e326f636747454a79756e66304849676c795a574e686348526a614745772b7336376f76332f2f2f2f2f415570714d4459774f575a6d4d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774d4441774e4749324f574d325a5455325a574e684d6a637a4d444e695a6d5a6d5a446b30595441774d4441774d4441774d44466d4e44497a4e545132596a6b324d6d49334d5755354e5749334f474a685a445a6c5954526b596a6b324e513d3d222c22733b32223a2235383432363833353330363230623830227d; _m_h5_tk=6b2d93ede46d8accf1e08330b01d10d8_1762174018109; _m_h5_tk_enc=2cb31d63275452aa75b254e96eb8c9bb; isg=BIOD8Vv07uI6PaIW3sswagFTEkct-Bc6vS4obbVg5eJidKKWPcoYipen7hw6VG8y; epssw=10*YdEss6_h_eQtk-xab-ds0vrR4I3PEqsGi88DbqssO-iQt6s3UR4Q-cgoU7IeQNFnbOzsssssssss638vq4q9r-Gjbu-jzAH6GHSPtekevO6az4rtspXYt55ssp3H8GRtvKpazHr2K5ifrkOVnsFY0ly4tTGNtzrtd1haQ-PODWYd-1f8tOJtiAicLLtfIij6zeTAruEVKQlJqBFO9DsjwsFOS-92dlWgkIJ4V0BniukNiWXQUiqRr6dsORrezQjL6A9vwO3TbRuZiGKHijJojdGACu44qMAsgA0mFGTuITVrHyydaQV4Ei2L8HLSAPhMxm95BC0QlAPQ-au0d-GUwfy.; tfstk=g2Aob4D6FLWSXgP7E2fSEQ0nNVMYV_1C4HFdv6IE3iSb2uFJ82fHrHAKPeoWxBjD8HIrqBLeiH-39LdRw9lHXethd4sdYMxp8L3x6fLWP6sFtcht6qugfU-u46Sr8t71WqQzq20x-61EXmLv6pNcO3xnwYBeuqbdRuPeYw74ui_dYw-F4trVSN1FYH-F3i7NRJzPza84ui_FTM-F8qfVcwfFYH5EoEl5XWSMTIOqAp5OA7s5OIblEG8mGWPH55BPbBj4TcRRrkSwziqUxG7HvELDy0V6k_OMjNK-g7xM8F9FnBqqjMODuQJelu0VsEvvBTvm4WjvwiB6a14EaEflqORVFzVWbEYeBtAx7f1lagJdNeUi2EAk2UODJyyVZ_pcIQfZ1uSpHFAh-BiIihYe5pWDtujyA-yNzSVCu2d4dJ6PlZj9KyOaQAoeye3moRM5UZ_-Xq00dJ6PlZjtoq2_VT7fycC..",
#     "VN": "lwrid=AgGW9hd%2Bw2Y12NSHQzfDX39uI%2BuO; lwrtk=AAIEaC8OEYcTvb0cYOV9WEvC/eAKF8OYcx3HHQo84j3AF8Ti3O08jq8=; isg=BI6OV_NAatcJ397zddZ6XSBI32RQD1IJtLZV6rjX0hFMGy51IJwoG3OQV193A0oh; epssw=9*mmCywmqUoOtdW2aimooYZpqiz374gSa4mmFOotSm3tZ3ecLR3tvO3tvOmoZO8trY4kQe4HD5IiHm5PTxsn6pVAMnI8oeJ-omItIu9LLunkKnM8La-O0fr4oGwgu93nOAoNAwJP9R55GMnYeV3memVuc0PWnlmmL0wRkjot7ufEjeh5vX2mvcKuWzHsRZh6zfQXhWTVH4ur02oWOwZrPY1uRzwOOyuuArd2FgItvOmmLR3QCXmA6RauLruSljiVzVJv7oIT_ksEBwECJvwSxBZkwq-vEtNnP4u-maXnepipwKCc6QvX5iXngeo9_bNG9.; tfstk=g_Sn5R4fRw8BZtF9WGtQoxh3pQzOdHt54_nJw3dz7CRs9XndU8xlK_j8dTJRr1X5iLQ8dQpzqCBYdUBFp02l1sYEyweBUafRsBPQAk1O6t1G2WZQA1C9_T5kPJOJaQfRUweTDoBCd3tyqSEYD6Yie-jHabKyAhShdXMLDoBCLFjoSdEA2Nj85BOy4e8EbfR6ED-yzeyM_LvjzX5PaRYwHpRraLue_cJW_Q-y4_WaILOwL3-rN2nyigS1b5G6FvYH3sjMKeAVIlirq1mv-I7es0PVjpmeg9Ri40RDloycI9FncOKCmsvA9lohiTWfzFjo_SA5jOSFzOG3QnXGWZLhSWok6Md9lM-mUkWMxBYVbeMnAsWGUZLGX-rXxHRFyH6-nWBGx6BCjTHr7HxdSEjH0oGewNBcqLj7NlfcUt_ySgch4BuZulliVwzhM4gW8d9MM1xUgXPkKWX4IR0bReJ6pSegI4gW8d9MMR2ilXTeCpFA.; x5sec=7b22617365727665722d6c617a6164613b33223a22617c434a2b4b75734547454a43387131306943584a6c5932467764474e6f5954442f797065612b502f2f2f2f3842536d6f774e6a41355a6d59774d4441774d4441774d4441304d4441774d4441774d4441774d4441774d4441774d4441774d4445774d444130597a45794e5449774e444a6b4d4459314e544d774e7a45355a57497a4f4455344d4441774d4441774d4441774d574d34596d51344e444d344e47526d4e6a51355a6a4d794e446333596d49354d6a51344e444e694f546c6b222c22733b32223a2237653232353332656535333162323631227d; hng=VN|vi|VND|704; hng.sig=zdydsNS1SsmgPDnK6hvJok_XUpANfcD7ya93aWHPt94",  # Vietnam
# }

lazada_domains = {
    "ID": "https://lazada.co.id",  # Indonesia
    "MY": "https://lazada.com.my",  # Malaysia
    "PH": "https://lazada.com.ph",  # Philippines
    "SG": "https://lazada.sg",  # Singapore
    "TH": "https://lazada.co.th",  # Thailand
    "VN": "https://lazada.vn",  # Vietnam
}

class LazadaShopSpider(PricemateBaseSpider):
    name = "lazada_shops"

    def __init__(self, retailer, region, *args, **kwargs):
        super().__init__(retailer=retailer, region=region, *args, **kwargs)
        self.domain = lazada_domains[self.region.upper()]
        self.cookies = lazada_cookies[f"cookies_{self.region.lower()}"]
        self.headers = lazada_cookies[f"headers_{self.region.lower()}"]
        # self.proxy_name = 'scrape_do'
        self.proxy_name = None

    def start_requests(self):

        docs = self.category_input.find({
            # "retailer": self.retailer,
            # "region": self.region,
            "Status": "Pending"
        })

        for doc in docs:
            url = doc["url"]
            hash_id = doc.get("_id")


            if '/shop/' in url:
                shop_id = url.split('/shop/shop/')[-1].split('/shop/')[-1].split('/')[0]
                filter_query = 'All-Products'

                url = f'{self.domain}/{shop_id}/?q={filter_query}&from=wangpu&langFlag=en&pageTypeId=2'
            else:
                shop_id = url.split(f"{self.domain[10:]}/")[-1].split('/')[0]
                filter_query = 'All-Products'
                url = f'{self.domain}/{shop_id}/?q={filter_query}&from=wangpu&langFlag=en&pageTypeId=2'
                print(url)
                print(url)
                # print("Please Check url...", StoreURL)
                # return

            page = 1
            if "?" in url:
                ajax_url = f"{url}&ajax=true&page={page}".replace('www.', '')
            else:
                ajax_url = f"{url}?ajax=true&page={page}".replace('www.', '')

            # hashid = generate_hashId(url)
            filename = f'{self.domain.split("//")[-1]}_{shop_id.replace("-", "_")}_page_{page}.json'

            yield scrapy.Request(
                url=ajax_url,
                headers=self.headers,
                cookies=self.cookies,
                callback=self.parse_pdp,
                meta={
                    "proxy_name" : self.proxy_name,
                    "main_url": url,
                    "hash_id":hash_id,
                    "ajax_url": ajax_url,
                    "shop_id": shop_id,
                    "filename": filename,
                    "page": page,
                    "should_be": ["mainInfo"]
                }

            )
    def parse_pdp(self, response):
        try:
            meta = response.meta
            url = meta.get('main_url')
            hash_id = meta.get('hash_id')
            ajax_url = meta.get('ajax_url')
            shop_id = meta.get('shop_id')
            filename = meta.get('filename')
            page = meta.get('page')
            should_be = meta.get('should_be')

            loaded_json = json.loads(response.text)

            totalResults = loaded_json['mainInfo']['totalResults']
            if int(totalResults) == 4080:
                totalResults = loaded_json['mods']['filter']['filteredQuatity']
                print("Max Page Limitation...", totalResults)

            product_list = loaded_json['mods']['listItems']

            if product_list:
                # process_thread(product_list)

                for pdp_data in product_list:

                    Parent_Id = pdp_data['itemId']
                    Product_Name = pdp_data['name']
                    itemid = pdp_data['skuId']
                    img = pdp_data['image']
                    try:
                        product_url = pdp_data['itemUrl'].split("?")[0]
                    except:
                        product_url = pdp_data['productUrl'].split("?")[0]

                    if not str(product_url).startswith("https"):
                        product_url = f"https:{product_url}"

                    seller_name = pdp_data['sellerName']
                    # seller_url = f"{domain}/{seller_name.lower().replace(' ', '-')}/?q=All-Products&from=wangpu&langFlag=en&pageTypeId=2"
                    try:
                        discount = pdp_data['discount']
                        pack_size = pdp_data['packageInfo']
                    except:
                        discount = ""
                        pack_size = ""
                    try:
                        originalPrice = float(pdp_data['originalPrice'])
                    except:
                        originalPrice = ""

                    try:
                        salePrice = float(pdp_data['price'])
                    except:
                        if originalPrice == salePrice:
                            # salePrice = originalPrice
                            originalPrice = ""

                        else:

                            print("Sale Price is required,,,,,", itemid)
                            return None

                    try:
                        stock_count = pdp_data['inStock']
                        if not stock_count:
                            isOos = True
                        else:
                            isOos = False
                    except:
                        isOos = False

                    item_sold = pdp_data.get('querystring', "") or pdp_data.get('productUrl', "")
                    if item_sold:
                        item_sold = int(item_sold.split("&sale=")[-1].split("&")[0])

                    ratingScore = pdp_data['ratingScore']
                    if ratingScore:
                        ratingScore = round(float(ratingScore), 1)

                    review = pdp_data['review']
                    if review:
                        review = int(review)

                    brand = pdp_data['brandName']
                    skuId = pdp_data['skuId']

                    currency = loaded_json['mainInfo']['currency']

                    sellerId = pdp_data['sellerId']
                    rrp = originalPrice
                    if originalPrice is None or originalPrice == "":
                        rrp = salePrice

                    breadcrumb_items = loaded_json.get('mods', {}).get('breadcrumb', [])
                    breadcrumb_titles = [crumb.get('title') for crumb in breadcrumb_items]
                    bread = ' > '.join(breadcrumb_titles)

                    product_hash = self.generate_hash_id(product_url, self.retailer, self.region)
                    item = {
                    "_id": product_hash,
                    "CategoryURL": url,
                    "HashID": hash_id,
                    "ProductCode": skuId,
                    "ParentCode": Parent_Id,
                    "ProductURL": product_url,
                    "Name": Product_Name,
                    "Brand": brand,
                    "Pack_size": pack_size,
                    "Price": salePrice,
                    "WasPrice": originalPrice,
                    "Category_Hierarchy":bread,
                    "is_available": True if not isOos else False,
                    "Status": "Done",
                    "Images": img,
                    "RRP": rrp,
                    "Offer_info": discount,
                    "Promo_Type": "",
                    "per_unit_price": "",
                    "Barcode": "",
                    "retailer": self.retailer,
                    "region": self.region,
                    "retailer_name" : self.RetailerCode,
                }
                    self.save_product(item)
                    # print(f"Product URL Inserted !")

            main_info = loaded_json.get('mainInfo', {})
            total_results = int(main_info.get('totalResults'))
            page_size = int(main_info.get('pageSize', 40))
            current_page = int(main_info.get('page', 1))

            total_pages = math.ceil(total_results / page_size)

            if page < total_pages:
                page = page + 1
                print("Going for next page..", page, "Expedited pages:", total_pages)
                if "?" in url:
                    ajax_url = f"{url}&ajax=true&page={page}".replace('www.', '')
                else:
                    ajax_url = f"{url}?ajax=true&page={page}".replace('www.', '')

                # hashid = generate_hashId(url)
                filename = f'{self.domain.split("//")[-1]}_{shop_id.replace("-", "_")}_page_{page}.json'
                token = "2192d06a19b74b23884d257fcffee6f696674f8e128"  # check_and_get_working_scrapedo_key()

                targetUrl = urllib.parse.quote(ajax_url)
                scrape_do_url = f'http://api.scrape.do?token={token}&url={targetUrl}&super=true'  # , proxies=proxies, verify="zyte-ca.crt"

                yield scrapy.Request(
                    url=ajax_url,
                    headers=self.headers,
                    cookies=self.cookies,
                    callback=self.parse_pdp,
                    meta={
                        "proxy_name" : self.proxy_name,
                        "main_url": url,
                        "hash_id":hash_id,
                        "ajax_url": ajax_url,
                        "shop_id": shop_id,
                        "filename": filename,
                        "page": page,
                        "should_be": ["mainInfo"]
                    }

                )
                return None

            else:
                self.category_input.update_one({"_id": hash_id}, {'$set':{'Status': "Done"}})
                print("Status Updated !")
                return None
        except Exception as e:
            print(e)
            return None

    def close(self, reason):
        self.mongo_client.close()

if __name__ == '__main__':
    from scrapy.cmdline import execute
    # execute("scrapy crawl lazada_shop -a retailer=lazada_id -a region=id -a Type=eshop -a RetailerCode=lazada_watsons_id".split())
    # execute("scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_my".split())
    execute("scrapy crawl lazada_shop -a retailer=lazada_ph -a region=ph -a Type=marketplace -a RetailerCode=lazada_ph".split())
    # execute("scrapy crawl lazada_shop -a retailer=lazada_ph -a region=ph -a Type=marketplace -a RetailerCode=lazada_watsons_ph".split())
    # execute("scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_bigpharmacy_my".split())
    # execute("scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_guardian_my".split())
    # execute("scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_petsmore_my".split())
    # execute("scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_mydin_my".split())
    # execute("scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_watsons_my".split())
    # execute("scrapy crawl lazada_shop -a retailer=lazada_my -a region=my -a Type=marketplace -a RetailerCode=lazada_caring_my".split())
    # execute("scrapy crawl lazada_shops -a retailer=lazada_id -a region=id -a Type=marketplace -a RetailerCode=lazada_id".split())
