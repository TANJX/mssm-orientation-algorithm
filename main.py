
def calculate(file):
  # read input files and return a list of lines (exclude first line)
  lines = open(file, 'r').read().strip().split('\n')[1:]

  # parse input lines and return a list of tuples (start, end)
  def splitNums(line):
      s = line.split(' ')
      return (int(s[0]), int(s[1]))
  guards = list(map(splitNums, lines))

  # sort by start time
  guards.sort(key=lambda x: x[0])

  # init
  latestEndTime = 0
  minUniqueTime = 1000000000
  minUniqueTimeIndex = 0


  for i in range(len(guards)):
    guard = guards[i]
    nextGuard = guards[i+1] if i+1 < len(guards) else (guard[1], guard[1])
    # if current guard time is competely covered by previous guard
    # break now
    if latestEndTime > guard[1]:
      minUniqueTime = 0
      minUniqueTimeIndex = i
      break
    # the duration of time that is uniquely covered by current guard
    currentUniqueTime = min(guard[1], nextGuard[0]) - latestEndTime
    # print(f'currentUniqueTime: {currentUniqueTime}')
    if currentUniqueTime < minUniqueTime:
      minUniqueTime = currentUniqueTime
      minUniqueTimeIndex = i
    if guard[1] > latestEndTime: # unneccessary, but for clarity
      latestEndTime = guard[1]
      # print(f'latestEndTime is now {latestEndTime}')


  # print(f'minUniqueTime: {minUniqueTime}')
  # print(f'minUniqueTimeIndex: {minUniqueTimeIndex}')

  del guards[minUniqueTimeIndex]

  f = open(f'test.out', 'w')
  f.write("\n".join(map(str, guards)))
  # calculate duration of time that is covered by guards excluded the one removed
  duration = 0
  i = 0

  lastIntervalEnd = 0
  while i < len(guards):
    guard = guards[i]
    startTime = guard[0]
    endTime = guard[1]
    if lastIntervalEnd > endTime:
      i += 1
      continue
    nextGuard = guards[i+1] if i+1 < len(guards) else None
    while nextGuard != None:
      if nextGuard[0] <= guard[1]:
        guard = nextGuard
        i += 1
        nextGuard = guards[i+1] if i+1 < len(guards) else None
        endTime = max(endTime, guard[1])
      else:
        endTime = max(endTime, guard[1])
        break
    duration += endTime - max(startTime, lastIntervalEnd)
    lastIntervalEnd = endTime
    # print(f'{duration} {endTime - startTime} ({startTime}, {endTime}) {i}')
    i += 1
  # print(f'duration: {duration}')
  return duration

# main function
if __name__ == '__main__':
  for i in range(10):
    f = open(f'output/{i+1}.out', 'w')
    result = calculate(f'input/{i+1}.in')
    f.write(f'{result}\n')
    f.close()