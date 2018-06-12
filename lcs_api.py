from flask import Flask, request, jsonify
import functools

app = Flask(__name__)


def substr(str1, str2):
    str1 = " ".join(i for i in str1) if type(str1) == set else str1
    len1 = len(str1)
    len2 = len(str2)
    count = [[0] * (len2 + 1) for x in range(len1 + 1)]
    longest = 0
    lcs_set = set()
    for i in range(len1):
        for j in range(len2):
            if str1[i] == str2[j]:
                c = count[i][j] + 1
                count[i + 1][j + 1] = c
                if c > longest:
                    lcs_set = set()
                    longest = c
                    lcs_set.add(str1[i - c + 1:i + 1])
                elif c == longest:
                    lcs_set.add(str1[i - c + 1:i + 1])

    return lcs_set


@app.route('/lcs', methods=['POST'])
def get_lcs():
    try:
        if request.data and request.data != "" and request.data != "{}":
            data = eval(request.data)
        else:
            raise Exception
    except:
        return jsonify({"error message": "The format of the request was not acceptable"}), 400

    if "setOfStrings" not in data or data["setOfStrings"] == '':
        return jsonify({"error message": "SetOfStrings should not be empty."}), 400

    values = [i["value"] for i in data["setOfStrings"]]

    if len(values) > len(set(values)):
        return jsonify({"error message": "'SetOfStrings' must be a Set"}), 400


    res = functools.reduce((lambda x, y: substr(x, y)), values)
    result = {}
    result["lcs"] = [{"value": i} for i in sorted(list(res))]
    return jsonify(result), 200


if __name__ == '__main__':
    app.run()
