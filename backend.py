
def upload_detection(request):
    # request['Access-Contro1-Allow-origin'] = "*"  # 设置请求头
    if request.method == 'POST':
        base_url = "http://" + request.META["HTTP_HOST"] + "/"
        files = request.FILES
        if files:
            ret = {'code': SUCCESS_CODE, 'message': SUCCESS_MESSAGE, 'urls': []}
            for fileName in files:
                file = request.FILES.get(fileName)
                # print("request.FILES.get(fileName):",file)
                # print(time.time())
                Rename, onlyFileName = rename(file)
                with open(Rename, 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                info = {'name': Rename, 'url': ""}
                ret['urls'].append(info)
            # opt = parse_opt()
            predict_dict = opt_run()
            print(predict_dict)
            data = {}
            data["code"] = 200
            data["res"] = predict_dict
            return JsonResponse(data)
        else:
            return JsonResponse("must be post")
