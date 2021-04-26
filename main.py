import csv


def normalizeSample(filename):
    """Normalizes the sample text file by performing:
    * a lowercase transformation
    * a deletion of special characters
    * a replacement of all ponctuation marks with white spaces

    Args:
        filename (str): the relative path of the file to be normalized
    """


def parseSample(filename):
    f = open(filename, "r")
    sampleString = f.read()
    sequenceMatrix = []
    for (indexChar, char) in enumerate(sampleString):
        if(indexChar != len(sampleString)-1):
            alreadyIn = False
            for sequence in sequenceMatrix:
                nextChar = sampleString[indexChar+1]
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
    allChars = []
    for sequence in sequenceMatrix:
        for i in range(0, 2):
            if not sequence[i] in allChars:
                allChars.append(sequence[i])
    allChars.sort()
    return allChars


# if __name__ == __main__:
sequenceMatrix = parseSample("samples/miserables.txt")
percentArray = sequenceMatrixToPercentage(sequenceMatrix)
csvFile = "sequences_sample.csv"
percentageMatrixToCSV(sequenceMatrix, percentArray, csvFile)
print(percentArray)
