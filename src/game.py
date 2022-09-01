import uasyncio

def val(buffer, x, y):
    #if (x >= 16 or x < 0 or y >= 16 or y < 0):
    #    return 0
    
    return buffer.get(x % 16, y % 16)


async def next_gen(current, target):
    target.clear()
    for i in range(0, 16):
        for j in range(0, 16):
            total = val(current, i-1, j-1) + val(current, i, j-1) + val(current, i+1, j-1) + val(current, i-1, j) + val(current, i+1, j) + val(current, i-1, j+1) + val(current, i, j+1) + val(current, i+1, j+1)
            if current.get(i, j):
                if (total < 2) or (total > 3):
                    target.set(i, j, 0)
                else:
                    target.set(i, j, 1)
            else:
                if total == 3:
                    target.set(i, j, 1)
                else:
                    target.set(i, j, 0)
        await uasyncio.sleep(0)
