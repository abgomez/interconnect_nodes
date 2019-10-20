import matplotlib.pyplot as plt
#plt.plot([110,120,130,140,150,160,170,180,190,200],[96,113,121,129,137,146,154,162,170,179])
cpu1 = [96,104,113,121,129,137,146,154,162,170,179]
cpu2 = [97,105,114,122,130,138,147,155,163,171,180]
cpu3 = [99,107,116,124,132,140,149,157,165,173,182]
cpu4 = [102,109,118,126,134,142,151,159,167,175,184]
cpu5 = [104,111,120,128,136,144,153,161,169,177,186]
cpu6 = [193,209,226,242,259,275,292,308,325,341,358]
cpu7 = [193,209,226,242,259,275,292,308,325,341,358]
cpu8 = [193,209,226,242,259,275,292,308,325,341,358]
buffer = [100,110,120,130,140,150,160,170,180,190,200]
fig, ax = plt.subplots()
# ax.scatter(buffer, cpu1, label="dog")
# ax.scatter(buffer, cpu2, label="cat")
# ax.scatter(buffer, cpu3, label="cat")
ax.plot(buffer, cpu5, label="cpu1-5", marker = "o")
ax.plot(buffer, cpu8, label="cpu6-8", marker = "*")
plt.xlabel("Buffer Size (in transactions)")
plt.ylabel("Capacity of validator nodes (in transactions/sec)")
plt.axhline(y=230, linewidth=1, color='k', label="Min. Capacity")
ax.legend()
plt.savefig('/home/abel/OneDrive/interconnect_nodes/capacity.eps', format='eps', dpi=1000)
#plt.show()




