import plistlib, sys, re, argparse
from matplotlib import pyplot as plt
import numpy as np
import statistics as stat

def findDuplicates(file):
    """
    Finds the duplicate songs in a playlist by comparing track name and duration and writing the duplicates to dups.txt
    """
    print(f"Finding duplicate tracks in {file}")
    # read in playlist
    plist = plistlib.readPlist(file)
    # get traacks from the Tracks dict 
    tracks = plist["Tracks"]
    # create a track name dict 
    trackNames = {}
    # loop through tracks
    for trackId, track in tracks.items():
        try:
            name = track["Name"]
            duration = track["Total Time"]
            # look for existing entries
            if name in trackNames:
                # if a name and duration match, increment count
                # round the track length to the nearest second
                if duration//1000 == trackNames[name][0]//1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count+1)
            else:
                trackNames[name] = (duration, 1)
        except:
            # ignore
            pass
    # store duplicates as (name, count) tuples       
    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))
        # save duplicates to a file
        if len(dups) > 0:
            print(f"Found {len(dups)} duplicates. Track names saved to dups.txt")
        else:
            print("No duplicate tracks found!")
        with open("dups.txt", "w") as f:
            for val in dups:
                f.write(f"[{val[0]}] {val[1]}\n")

def findCommonTracks(files):
    """
    Determine if which tracks are in common between playlists using the track name and duration and writing the matching tracks to common.txt
    """
    # a list of sets of track names
    trackNameSets = []
    for file in files:
        # create new set
        trackNames = set()
        # read in playlist
        plist = plistlib.readPlist(file)
        # get tracks
        tracks = plist["Tracks"]
        # iterate through tracks
        for trackId, track, in tracks.items():
            try:
                name = track["Name"]
                duration = track["Total Time"]
                trackInfo = (name, duration)
                trackNames.add(trackInfo)
            except:
                pass
            trackNameSets.append(trackNames)
        # get set of common tracks
        commonTracks = set.intersection(*trackNameSets)
        # write to file
        if len(commonTracks) > 0:
            with open("common.txt", "wb") as f:
                for val in commonTracks:
                    s = "%s\n" % val[0]
                    f.write(s.encode("utf-8"))
            print(f"{len(commonTracks)} common tracks found. "
                    "Track names written to common.txt.")
        else:
            print("No common tracks!")

def plotStats(file):
    """
    Plot some statistics by reading track information from a playlist
    """
    # read playlist
    plist = plistlib.readPlist(file)
    # get tracks from playtlist
    tracks = plist["Tracks"]
    # create lists of song plays and track duration
    plays = []
    durations = []
    # iterate through tracks
    for trackId, track in tracks.items():
        try:
            plays.append(track["Play Count"])
            durations.append(track["Total Time"])
        except:
            pass   
    # make sure data collected was valid
    if plays == [] or durations == []:
        print(f"No valid Play Count/Total Time data in {file}")
        return

    # calculate correlation coeffecient
    # first calculate the means of the two data sets
    mean_durations = stat.mean(durations)
    mean_plays = stat.mean(plays)
    # correlation is covariance/stdev_x * stdev_y
    covariance = 0
    for play, dur in zip(plays, durations):
        covariance = covariance + (play - mean_plays) * (dur - mean_durations)
    covariance = covariance / len(plays) - 1
    stdev_durations = stat.stdev(durations, mean_durations)
    stdev_plays = stat.stdev(plays, mean_plays)
    correlation = covariance / (stdev_durations * stdev_plays)

    # scatter plot
    x = np.array(durations, np.int32)
    # convert to minutes
    x = x/60000.0
    y = np.array(plays, np.int32)
    plt.subplot(2, 1, 1)
    plt.plot(x, y, "o")
    plt.axis([0, 1.05*np.max(x), -1, 110])
    plt.xlabel("Track duration")
    plt.ylabel("Track plays")
    plt.text(1, 90, r'$Cov$ = %f' % covariance)
    plt.text(1, 80, r"$r$ = %f" % correlation)

    # plot histogram
    plt.subplot(2, 1, 2)
    plt.hist(x, bins=20)
    plt.xlabel("Track duration")
    plt.ylabel("Count")

    # show plot
    plt.show()

def main():
    # create parser 
    descStr = """
    This program analyzes playlist files (.xml) exported from iTunes
    """
    parser = argparse.ArgumentParser(description=descStr)
    # add a mutually exclusive group of arguments
    group = parser.add_mutually_exclusive_group()

    # add expected arguments
    group.add_argument('--common', nargs="*", dest="plFiles", required=False)
    group.add_argument("--stats", dest="plFile", required=False)
    group.add_argument('--dup', dest="plFileD", required=False)

    # parse args
    args = parser.parse_args()

    if args.plFiles:
        # find common tracks
        findCommonTracks(args.plFiles)
    elif args.plFile:
        # plot stats
        plotStats(args.plFile)
    elif args.plFileD:
        #find duplicate tracks
        findDuplicates(args.plFileD)
    else:
        print("These are not the tracks you are looking for.")

# main method 
if __name__ == "__main__":
    main()

