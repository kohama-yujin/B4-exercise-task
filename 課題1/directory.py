import glob

# 階層構造
def run():
    filepath = ''
    while True:
        files = glob.glob(filepath + '*') # ファイル一覧取得
        if len(files) == 0:
            break
        print('----------------------')
        print("0 ： ..")
        for index, file in enumerate(files):
            print(index+1, '：', file)
        print('----------------------')

        print('どこを開きますか？')
        num_file = int(input())

        # ファイルパス更新
        if num_file == 0:
            filepath = filepath + "../"
        else:
            filepath = files[num_file-1] + "/"

    return filepath[:-1]