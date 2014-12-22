import soundDownload as SD

# Search and download top 20 relevant search results for violin
SD.downloadSoundsFreesound(queryText='violin', API_Key='e6c6932d9217cd4a6e99a80d56c74cf265449e7a', outputDir='testDownload', topNResults=20, duration=(0,5), tag='single-note')

# Search and download top 20 relevant search results for guitar
SD.downloadSoundsFreesound(queryText='guitar', API_Key='e6c6932d9217cd4a6e99a80d56c74cf265449e7a', outputDir='testDownload', topNResults=20, duration=(0,5), tag='1-shot')

# Search and download top 20 relevant search results for trumpet
SD.downloadSoundsFreesound(queryText='trumpet', API_Key='e6c6932d9217cd4a6e99a80d56c74cf265449e7a', outputDir='testDownload', topNResults=20, duration=(0,5), tag='single-note')
