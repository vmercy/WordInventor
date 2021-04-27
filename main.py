import csv
import random
import time
import json


def normalizeSample(filename):
    """Normalizes the sample text file by performing:
    * a lowercase transformation
    * a deletion of special characters
    * a replacement of all ponctuation marks with white spaces

    Args:
        filename (str): the relative path of the file to be normalized
    """
    pass


def parseSample(filename):
    """Generates the sequence matrix by reading a normalized file

    Args:
        filename (string): the relative path of the file to be analyzed

    Returns:
        array: the sequence matrix resulting of the analysis
    """
    f = open(filename, "r")
    sampleString = f.read()
    sequenceMatrix = []
    for (indexChar, char) in enumerate(sampleString):
        if(indexChar != len(sampleString)-1):
            nextChar = sampleString[indexChar+1]
            # TODO: move to normalize function and allow white space
            if not (ord(char) in range(ord('a'), ord('z')+1)) or not (ord(nextChar) in range(ord('a'), ord('z')+1)):
                continue
            alreadyIn = False
            for sequence in sequenceMatrix:
                if (sequence[0] == char) and (sequence[1] == nextChar):
                    sequence[2] += 1
                    alreadyIn = True
                    break
            if not alreadyIn:
                sequenceMatrix.append(
                    [char, sampleString[indexChar+1], 1])
    return sequenceMatrix


def sequenceMatrixToPercentage(sequenceMatrix):
    """Turns the sequence matrix into a percentage matrix representing, for each charachter, the probability of a second charchater to follow the first

    Args:
        sequenceMatrix (array): the multidimensional sequence matrix

    Returns:
        array: the multidimensional percentage matrix
    """
    percentArray = []
    leftHandChars = []
    for sequence in sequenceMatrix:
        if not leftHandChars.__contains__(sequence[0]):
            leftHandChars.append(sequence[0])
            subPercentArray = []
            for sequenceBis in sequenceMatrix:
                if sequenceBis[0] == sequence[0]:
                    subPercentArray.append(
                        [sequenceBis[1], sequenceBis[2]])
            percentArray.append([sequence[0], subPercentArray])
    for element in percentArray:
        totalSequences = 0
        for subElement in element[1]:
            totalSequences += subElement[1]
        for subElement in element[1]:
            subElement[1] /= float(totalSequences)
    return percentArray


def percentageMatrixToJson(percentageMatrix, filename):
    """Writes a JSON file to save the percentage matrix

    Args:
        percentageMatrix (array): the percentage matrix
        filename (string): output file relative path
    """
    with open(filename, "w") as outfile:
        json.dump(percentageMatrix, outfile)


def jsonToPercentageMatrix(filename):
    """Reads a JSON file with the percentage matrix encoded inside

    Args:
        filename (string): input file relative path
    Returns:
        array: the percentage matrix read
    """
    with open(filename, "r") as inputfile:
        percentageMatrix = json.load(inputfile)
        return percentageMatrix


def percentageMatrixToCSV(sequenceMatrix, percentageMatrix, targetFilename):
    """Writes a CSV file with a 2-Dim representation of the percentage matrix

    Args:
        sequenceMatrix (array): the sequence matrix
        percentageMatrix (array): the percentage matrix
        targetFilename (string): the target filename
    """
    allChars = getAllChars(sequenceMatrix)
    header = ['']+allChars
    rows = []
    for previous in allChars:
        nextCharPercentages = []
        for percentSubArray in percentageMatrix:
            if percentSubArray[0] == previous:
                nextCharPercentages = percentSubArray[1]
                break
        newRow = [previous]+len(header)*[0]
        rows.append(newRow)
        for next in nextCharPercentages:
            rows[allChars.index(previous)][1+allChars.index(next[0])] = next[1]

    with open(targetFilename, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
        writer.writerows([header]+rows)


def getAllChars(sequenceMatrix):
    """Generates a list containing all analyzed characters. Each character appears only once.

    Args:
        sequenceMatrix (array): the sequence matrix

    Returns:
        array: array containing all analyzed characters with no duplicate
    """
    allChars = []
    for sequence in sequenceMatrix:
        for i in range(0, 2):
            if not sequence[i] in allChars:
                allChars.append(sequence[i])
    allChars.sort()
    return allChars


def generateWord(percentageMatrix, length):
    """Generates a new unexisting word following Markov Chains of percentageMatrix

    Args:
        percentageMatrix (array): the percentage matrix
        length (int): the desired length of generated word

    Returns:
        string: the generated word
    """
    previous = random.choice(percentageMatrix)
    word = previous[0]
    for i in range(0, length-1):
        charWeights = []
        for next in previous[1]:
            charWeights.append(next[1])
        selectedChar = random.choices(previous[1], weights=charWeights)[0]
        word += selectedChar[0]
        found = False
        for char in percentageMatrix:
            if char[0] == selectedChar[0]:
                previous = char
                found = True
        if not found:
            exit

    return word


if __name__ == "__main__":
  """ TO ANALYZE A SAMPLE TEXT : """
  sequenceMatrix = parseSample("samples/german.txt")
  percentArray = sequenceMatrixToPercentage(sequenceMatrix)
  csvFile = "sequences_sample.csv"
  percentageMatrixToCSV(sequenceMatrix, percentArray, csvFile)
  JSONFile = "percentage_matrix.json"
  percentageMatrixToJson(percentArray, JSONFile)


  """ TO LOAD AN EXISTING ANALYSIS
  percentArray = jsonToPercentageMatrix("percentage_matrix.json")
  """

print("********* GENERATED WORDS : *********")
for i in range(0, 10):
    print(generateWord(percentArray, 7))
