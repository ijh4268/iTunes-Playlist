import plistlib, matplotlib

def findDuplicates(file):
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
        for trackId, track in tracks.items():
            try:
                trackNames.add(track["Name"])
            except:
                pass
            trackNameSets.append(trackNames)
        # get set of common tracks
        commonTracks = set.intersection(*trackNameSets)
        # write to file
        if len(commonTracks) > 0:
            with open("common.txt", "w") as f:
                for val in commonTracks:
                    f.write(f"{val}".encode("UTF-8"))
            print(f"{len(commonTracks)} common tracks found. "
                    "Track names written to common.txt.")
        else:
            print("No common tracks!")

    