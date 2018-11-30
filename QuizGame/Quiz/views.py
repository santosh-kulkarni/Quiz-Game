from django.shortcuts import render, redirect
import urllib
import json


total_list = []


def first_page(request):
    total_list.clear()
    request.session["val"] = -1
    request.session["total"] = -1
    request.session["correct"] = 0
    return render(request, "homepage.html", )


def replace(string):
    return string.replace("&quot;", "").replace("&#039;", "").replace("&Eacute;", "")


def print_answer(lst):
    for val in lst:
        print(val["question"] + " " + val["answer"] + " " + val["your_answer"] + " " + str(val["status"]))


def show_question(request):

    if request.session["val"] != -1:
        datavalue = request.POST.dict()
        index = int(request.session["val"])
        if datavalue["optradio"] == datavalue["button"]:
            request.session["correct"] += 1
            total_list[index]["status"] = True
        total_list[index]["your_answer"] = datavalue["optradio"]
        request.session["val"] = request.session["val"] + 1
        value = int(request.session["val"])
        if value == len(total_list):
            print_answer(total_list)
            accuracy = float(request.session["correct"]) / float(request.session["total"]) * float(100)
            return render(request, "finish.html", {"total_correct": accuracy, "Total_Q": request.session["total"], "Correct_Ans": request.session["correct"], "details": total_list})
        return render(request, "questions.html", {"Total_List": total_list[value], "num": value+1})

    else:
        data = request.POST.dict()
        number = data["number"]
        request.session["total"] = number
        cat = data["cat"]
        if cat == "Select Category..":
            return redirect("/quiz/", {"Message": "Please Select A Category"})

        if cat == "General Knowledge":
            cat = 9
        elif cat == "Sports":
            cat = 21
        elif cat == "Politics":
            cat = 24
        elif cat == "Science : Computer":
            cat = 18
        elif cat == "History":
            cat = 23
        elif cat == "Science : Mathematics":
            cat = 19

        level = data["level"]
        if level == "Difficulty Level..." or level == "Easy":
            level = "easy"
        elif level == "Medium":
            level = "medium"
        else:
            level = "hard"

        url = "https://opentdb.com/api.php?amount="
        url = url + str(number)
        url = url + "&category="
        url = url + str(cat)
        url = url + "&difficulty="
        url = url + level
        url = url + "&type=multiple"

        with urllib.request.urlopen(url) as u:
            jsondata = json.loads(u.read().decode())
        k = 0

        for val in jsondata["results"]:
            temp_ans = []
            for incorrect in val["incorrect_answers"]:
                temp_ans.append(replace(incorrect))
            temp_ans.append(replace(val["correct_answer"]))
            temp_ans.sort()
            temp = {
                "question": replace(val["question"]),
                "answer": replace(val["correct_answer"]),
                "your_answer": "",
                "status": False,
                "options": temp_ans
            }
            total_list.append(temp)
            k = k + 1
        request.session["val"] = 0
        send = total_list[0]
        return render(request, "questions.html", {"Total_List": send, "num": 1})
