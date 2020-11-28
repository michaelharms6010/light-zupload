import subprocess
import time
import json

file = input("enter the name of the file that you'd like to save and share via the zcash blockchain: ")

text = open(file,"r") 

input_file = text.read()
# input_file = text.read().split(" ")

# cur = 0
# current_memo_length = 0
# memos = []
# words = []
# while cur < len(input_file):
#     if len(" ".join(words)) + len(input_file[cur]) > 500:
#         memos.append(" ".join(words))
#         words = []
#     else:
#         words.append(input_file[cur])
#         cur += 1

# memos.append(" ".join(words))

chunks, chunk_size = len(input_file), 500
memos = [ input_file[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
memos.append("-- END OF DATA --")

new_zaddr = json.loads(subprocess.check_output("zecwallet-cli new z", shell=True))[0]
# new_zaddr = "zs1w2yjv5l09qcsyjpup3gydc9whr6afvdfjwf2lrs67pquhustasu8vhftza7smzdhfxyvjlh7y99"
print("Sending your text to a new zaddr: " + new_zaddr)
# view_key = "zxviews1qw763mfqzgqqpqp7wzjt00dsjhl3d4t638lvq3hwslsy9qejjpv3j4psjmuejfcp4srkxcgeh3x2v0urr0lfy6cean04e73d8ktzefr7fv0wem46474mnyn4k4mz4vlrgmchahj2qrdyn20heusaruaj87c9dzy4ggneapcvr20wcr0067m5a47ql3n9ux0uaweerlycj5gqwn0cmew7kja7r373gv0qqq6yjte5x955agexxdpjwcygjgpvsn4g4kay4fwe09wjqhgw2xyzk"
view_key = json.loads(subprocess.check_output(f"zecwallet-cli export {new_zaddr}", shell=True))[0]["viewing_key"]
print("After the sending completes, you can view your content using the viewing key: " + view_key)
count = 0
done = False
h = {}
while not done:
    spendable_balance = 0

    while spendable_balance < 10000:
        spendable_balance = json.loads(subprocess.check_output(f"zecwallet-cli balance", shell=True))["spendable_zbalance"]
        time.sleep(15)
    tx = subprocess.check_output(f"zecwallet-cli send {new_zaddr} 0 \"{memos[count]}\"", shell=True) # probably ['txid']
    print(tx)
    tx = tx.decode("utf-8") 
    
    
    if "Error:" not in tx and "Insufficient verified" not in tx:
        new_transaction = json.loads("{" + tx.split("\n{")[-1])
        txid = new_transaction["txid"]
        print ("sent tx", txid)
        if not h.get(txid):
            if memos[count] == "-- END OF DATA --":
                done = True
            count += 1
            h[txid] = 1
        print(f"memo {count} of {len(memos)} sent")
    else:
        print("tx issue")

    time.sleep(40)
    

balance = json.loads(subprocess.check_output(f"zecwallet-cli balance", shell=True))

print(balance)

# return view key and success message when done

# print(f"Finished sending {count} memo/s to {new_zaddr}.\n They are archived forever and viewable via your new viewing key:\n{view_key}")


x = subprocess.check_output("echo Hello World", shell=True)

print(x)