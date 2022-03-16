def build(winners):
    msg = winners[0]
    
    if len(winners) > 1:
        for i in range(1,len(winners)-1):
            msg += ", " + winners[i]
        msg += " and " + winners[len(winners)-1]

    return msg

print(build(["a","b","c","d"]))
print(build(["a","b","c"]))
print(build(["a","b"]))
print(build(["a"]))
