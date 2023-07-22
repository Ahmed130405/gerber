import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

prcs = pd.read_csv('tryingstuff/prcs.csv')
print(prcs.head())
# assets = [SPX,RTY,M1EA,EM,XAU,SPGSCI,LF98TRUU,LBUSTRUU,FNERTR]
assets = []
for i in range(1,10):
    asset_to_append = prcs.iloc[:,i].tolist()
    assets.append(asset_to_append)
print(assets[0])

c = 1

signals = []
timescale = len(assets[0])
timescale_minus_lookback = timescale-252

for i in range(len(assets)):
    signal_to_append = []
    for j in range(timescale_minus_lookback):
        one_year_period = assets[i][j:j+252]
        prc_ratio = assets[i][j+252]/np.percentile(one_year_period,90)
        if prc_ratio>c:
            signal_to_append.append(1)
        elif prc_ratio<-c:
            signal_to_append.append(-1)
        else:
            signal_to_append.append(0)
    signals.append(signal_to_append)
print(len(signals[0]))

correlation_data=[]

for i in range(len(assets)):
    correlation_data.append([])

for i in range(len(assets)):
    for j in range(len(assets)):
        if i>=j:
            correlation_data[i].append(0)
        else:
            useless_dict={
                1:-1,
                -1:1
            }
            concordant=0
            discordant=0
            neutral=0
            ignore=0
            for k in range(len(signals[0])):
                if signals[i][k] in useless_dict:
                    if signals[j][k] == useless_dict[signals[i][k]]:
                        discordant+=-1
                    elif signals[j][k] == signals[i][k]:
                        concordant+=1
                    else:
                        neutral+=1
                else:
                    if signals[j][k] == signals[i][k]:
                        ignore+=1
                    else:
                        neutral+=1
            gerby = (concordant-discordant)/(len(signals[0])-ignore)
            correlation_data[i].append(gerby)

# List of asset labels
asset_labels = ['SPX','RTY','M1EA','EM','XAU','SPGSCI','LF98TRUU','LBUSTRUU','FNERTR']

# Create a DataFrame from the correlation data
df_corr = pd.DataFrame(correlation_data, columns=asset_labels, index=asset_labels)

# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(8, 6))

# Create the heatmap using Seaborn's heatmap function
sns.heatmap(df_corr, annot=True, cmap='coolwarm', fmt=".2f", center=0, linewidths=0.5, ax=ax)

# Add labels, title, and adjust the plot
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
ax.set_title('Pairwise Correlations of Assets')
plt.tight_layout()

plt.savefig('tryingstuff/figure1.png')

# Show the plot
plt.show()