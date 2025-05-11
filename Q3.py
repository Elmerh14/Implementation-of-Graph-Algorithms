from heapq import heappush, heappop, heapify
from collections import defaultdict
from bitarray import bitarray, decodetree
import math
import os

def getFrequency(filePath):
    freq = defaultdict(int)
    with open(filePath) as file:
        for line in file:
            for word in line:
                freq[word] += 1
    return freq
        

def huffmanCode(aDict):   #with a given dictionary
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[freq, [aChar, ""]] for aChar, freq in aDict.items()]  # build a minheap
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)  # pop least frequent, then heapify
        hi = heappop(heap)  # next least frequent , then heapify
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]  #pair[1] is the current codeword for pair[0] char
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:]) #push then heapify

    #return huffman code dictionary with bitarray values
    return {char: bitarray(code) for char, code in heappop(heap)[1:]}




def zip(text, fileName, huffmanDict):
    #Read the text file content
    with open(text) as f:
         file = f.read()

    #Encode text to bit string using Huffman code table
    encodedBits = bitarray()
    for char in file:
        encodedBits.extend(huffmanDict[char]) #append the huffman bits
    
    #write to a binary .zip file
    with open(fileName, 'wb') as f:
        encodedBits.tofile(f) #write as binary
    
    #print the zip size
    zipSize = os.path.getsize(fileName)
    print(f"Compressed file written to '{fileName}'")
    print(f"Compressed file size: {zipSize} bytes")

    return encodedBits, zipSize  # needed for unzip later


def unzip(zipFileName, huffman, zipSize):
    #open and read zipped binary file
    with open(zipFileName, "rb") as file:
        bitStream = bitarray()
        bitStream.fromfile(file)
    #trim the padding bits that were added to align to full bytes
    bitStream = bitStream[:zipSize]

    #build decoding tree from the huffman dictionary
    decodedTree = decodetree(huffman)

    #decode the bit stream into characters
    decodedText = bitStream.decode(decodedTree)

    #write the decoded string to a text file
    outPutFile = zipFileName.replace('.zip', '.unzipped.txt')
    with open(outPutFile, 'w', encoding='utf-8') as out:
        out.write(''.join(decodedText))

    #print the file size
    unzippedSize = os.path.getsize(outPutFile)
    print(f"Unzipped file written to '{outPutFile}'")
    print(f"Unzipped file size: {unzippedSize} bytes")

def printHuffmanStats(freqDict, huffDict):
    print(f"\n{'Character':<12} {'Weight':<15} {'Huffman Code'}")
    totalHuffCost = 0
    totalAsciiCost = 0 
    totalFreq = sum(freqDict.values())

    #print code table and calculate cost of each symbol
    for char, code in sorted(huffDict.items(), key=lambda x: (len(x[1]), x[0])):
        freq = freqDict[char]
        cost = freq * len(code)
        totalHuffCost += cost
        totalAsciiCost += freq * 8
        displayChar = repr(char) if char == '\n' else char
        print(f"{displayChar:<12} {freq:<15} {code}")

    #calculate cost of optimal fixed length coding
    numSymbols = len(freqDict)
    fclCost = int(totalFreq * math.ceil(math.log2(numSymbols)))

    #print the compression stats
    print(f"\nExpected cost of Huffman code: {totalHuffCost}")
    print(f"Expected cost of ASCII: {totalAsciiCost}")
    print(f"Huffman efficiency improvement over ASCII: {round(100 * (1 - totalHuffCost / totalAsciiCost), 2)}%")
    print(f"Expected cost of optimal FCL: {fclCost}")
    print(f"Huffman efficiency improvement over FCL: {round(100 * (1 - totalHuffCost / fclCost), 2)}%")


def main():
    fileName = input("Enter a file name to encode: ")
    if not os.path.exists(fileName):
        print("File not found.")
        return
    
    #build the frequency table and the huffman code dictionary
    frequency = getFrequency(fileName)
    huffmanDict = huffmanCode(frequency)

    #pring huffman code table and efficency stats
    printHuffmanStats(frequency, huffmanDict)

    #show the original file size 
    originalSize = os.path.getsize(fileName)
    print(f"\nThe size of {fileName}: {originalSize} bytes")

    #compress the file and show the size of the compression
    outputZipFile = fileName.split('.')[0] + '.zip'
    bitstream, zipSize = zip(fileName, outputZipFile, huffmanDict)
    print(f"The size of {outputZipFile}: {zipSize} bytes")

    #decompress the file and print the size
    unzip(outputZipFile, huffmanDict, len(bitstream))
    unzippedFile = outputZipFile.replace('.zip', 'unzipped.txt')
    if os.path.exists(unzippedFile):
        unzippedSize = os.path.getsize(unzippedFile)
        print(f"The size of {unzippedFile}: {unzippedSize} bytes")


if __name__ == "__main__":
    main()