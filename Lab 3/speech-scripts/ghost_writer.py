#!/usr/bin/env python3

# prerequisites: as described in https://alphacephei.com/vosk/install and also python module `sounddevice` (simply run command `pip install sounddevice`)
# Example usage using Dutch (nl) recognition model: `python test_microphone.py -m nl`
# For more help run: `python test_microphone.py -h`

import argparse
import queue
import sys
import sounddevice as sd

from vosk import Model, KaldiRecognizer

q = queue.Queue()
nl = []
content = []
status = None
rewriteBegin = False
newSentence = None
replaceidx = 0
deleteidx = 0
# lastIndex = len(nl)-1

def output_content(c):
    for i in range(len(c)-1):
        if(c[i][-1] != "."):
            c[i] = c[i] + "."
    output_text = " ".join(c)
    return output_text

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def sentence_to_words(newSentence):
    newSentence = newSentence[14:-3]
    words = newSentence.split()
    global rewriteBegin
    global replaceidx
    global deleteidx
    # global lastIndex
    # lastIndex = len(content)-1
    if "show me everything" in newSentence:
        print(content)
        # print(output_content(content))
        return
    if "delete" in newSentence and len(words) == 1:
        # content.remove(lastIndex)
        content.pop()
        print(content)
        return
    # if words == ["pie","delete"] and lastIndex > 0:
    #     content.remove(lastIndex)
    if "delete" in newSentence and len(words) > 1:
        try:
            deleteidx = int(help_dict[words[-1]])-1
            print(deleteidx)
            content.pop(deleteidx)
            print(content)
        except:
            print("error listening")
        # print(deleteidx)
        # replaceidx = help_dict[newSentence[newSentence.rfind():-1]]-1
        # content.pop(deleteidx)
        return
    if "back" in newSentence:
        lllist = content[-1].split()
        lllist = lllist[:-1]
        # print (lllist)
        content[-1] = " ".join([str(item) for item in lllist])
        print(content)
        # print("content",content)
        return
    # if words == ["pie","backspace"] and lastIndex > 0:
    #     content[lastIndex]= content[lastIndex][:len()-1]
    if "rewrite" in newSentence:
        # status = "rewrite"
        rewriteBegin = True
        try:
            replaceidx = int(help_dict[words[-1]])-1
            content.pop(replaceidx)
            print(content)
        except:
            print("error listening")
        print(replaceidx)
        # replaceidx = help_dict[newSentence[newSentence.rfind():-1]]-1
        # content.pop(replaceidx)
        return
    # if status == "rewrite":
    if rewriteBegin == True:
        content.insert(replaceidx, newSentence)
        # status = None
        rewriteBegin = False
    else:
        if len(newSentence)!=0:
            content.append(newSentence)
        replaceidx = 0
        print(content)
    # if status == continue

help_dict = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero': '0',
    'ten': '10',
    'eleven': '11',
    'twelve': '12'
}

# def ghost_analyze():
    
# def output_content(c):
#     output_text = ". ".join(c)
#     return output_text

def string_to_int(newlist):
    
    # content = newlist[0][14:len(newlist[0])-3]
    # content.split()
    try:
        content = newlist[0][14:len(newlist[0])-3]
        res = ''.join(help_dict[ele] for ele in content.split())
        print("your number is")
        print(res)
    except:
        print("You didn't give me the correct response")
    # print("your number is")
    # print(res)


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        model = Model(lang="en-us")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("\nStart saying things you want to write down, sentence by sentence;\nSay 'BACK' to delete the last element; \nSay 'DELETE' to delete the last sentence; \nSay 'DELETE+ [number]' to delete sentence [number]; \nSay 'REWRITE+ [number]' to rewrite sentence [number]\n")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            # replaceidx = 0
            if rec.AcceptWaveform(data):
                newSentence = rec.Result()
                if newSentence[14:-3] != "":
                    print("Your Sentence: " + newSentence[14:-3])
                # content.append(newSentence[14:-3])
                sentence_to_words(newSentence)
                # if "pie rewrite sentence" in rec.Result():
                #     status = "rewrite"
                #     replaceidx = help_dict[rec.Result[rec.Result.rfind():-1]]-1
                #     content.pop(replaceidx)
                # print(type(rec.Result()))
                # nl.append(rec.Result())
                # print(nl)
                # if status == "rewrite":
                #     content.insert(replaceidx, rec.Result())
                #     status = None



                # print(rec.Result())
                # nl.append(rec.Result())
            # else:
            #     # print(rec.PartialResult())
            #     return
            if dump_fn is not None:
                dump_fn.write(data)
                

except KeyboardInterrupt:
    # string_to_int()
    print("\n")
    # print(nl)
    # string_to_int(nl)
    # print(content)
    print(output_content(content))
    print("\nThe End")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
