const fs = require("fs");
const demofile = require("demofile");

// aliases console.log to clog
function clog(text) {
    console.log(text)
}

// marks start time of program running in completed.txt
fs.appendFileSync('./completed.txt', `\nnewlaunch ${Math.floor(Date.now() / 1000)}`, function (err) {
    if (err) {
        fs.writeFileSync('./completed.txt', `\nnewlaunch ${Math.floor(Date.now() / 1000)}`, function (err) { })
    }
});

// reads all files in demofiles (directory containing demo files)
fs.readdir("./demofiles", (err, files) => {
    if (err) throw err
    files.forEach(file => {
        console.log(`${file} is beginning parsing`)
        // variables containing information about the match
        let kds = {} // kill to death ratios of all players in the match
        let matchstart = false, roundstart = false, roundend = false, bombplant = false
        let timecount = 0, showtick = false, stillrunning = true // timecount counts the amount of time the program has been running for
        let spottedListT = [], spottedListCT = [] // list of players the t and ct side have spotted respectively
        let spottedListTtemp = [], spottedListCTtemp = [] // temporary list of above

        const fname = file.substr(0, file.length - 4) // strips file extension .demo

        if (!fs.existsSync(`./results/${fname},results`)) {
            fs.mkdirSync(`./results/${fname},results`);
        }

        fs.readFile(`./demofiles/${fname}.dem`, (err, buffer) => {
            const demo_file = new demofile.DemoFile()

            demo_file.gameEvents.on("round_announce_match_start", e => {
                matchstart = true
                clog("match start")
                var interval = setInterval(function () { // prints time elapsed for reading the demo file every minute
                    timecount++
                    console.log(`${timecount}mins elapsed\n`)
                    showtick = true
                    stillrunning = false
                    setTimeout(() => {
                        if (!stillrunning) { // demo file has been parsed
                            clearInterval(interval)
                            console.log(`${fname} has been parsed`)
                            fs.appendFileSync('./completed.txt', `\n${fname} has been parsed`, function (err) {
                            });
                        }
                    }, 5000)
                }, 60000)
            })


            demo_file.gameEvents.on("round_start", e => {
                if (matchstart) {
                    roundstart = true
                    roundend = false
                }
            })

            demo_file.gameEvents.on("round_end", e => {
                if (matchstart) {
                    roundstart = false
                    roundend = true
                    bombplant = false
                    // iterates over all players
                    for (let x = 0; x < demo_file.entities.players.length; x++) {
                        let pl = demo_file.entities.players[x]
                        if (pl.steam64Id == 0) { // ignores players with invalid ids
                            continue
                        }
                        if (pl.teamNumber == 0 || pl.teamNumber == 1) { // ignores spectators
                            continue
                        }
                        let newkd
                        if (pl.kills == 0) {
                            newkd = 0
                        } else if (pl.deaths == 0) {
                            newkd = pl.kills + 1
                        } else {
                            newkd = Math.round(pl.kills / pl.deaths * 100) / 100
                        }
                        newkd = String(newkd)
                        // turns newkd into kd of the right format x,xx
                        if (newkd.length == 1) {
                            newkd = newkd + ".00"
                        } else if (newkd.length == 3) {
                            newkd = newkd + "0"
                        }
                        newkd = newkd.replace(".", ",")
                        // renames player file the program is outputting info to to the right kd
                        fs.rename(`./results/${fname},results/${fname},${pl.steam64Id},${kds[pl.steam64Id]}`, `./results/${fname},results/${fname},${pl.steam64Id},${newkd}`, (err) => {
                        })
                        kds[pl.steam64Id] = newkd
                    }

                }
            })

            demo_file.gameEvents.on("bomb_planted", e => { // event switches the hold condition
                if (matchstart) {
                    bombplant = true
                }
            })

            demo_file.on("tickend", e => {
                if (showtick) {
                    clog(e)
                    showtick = false
                    stillrunning = true
                }
                if (roundstart) {
                    for (let x = 0; x < demo_file.entities.players.length; x++) {
                        let pl = demo_file.entities.players[x]
                        if (pl.steam64Id == 0) { // ignores invalid ids
                            continue
                        }
                        if (pl.teamNumber == 0 || pl.teamNumber == 1) { // ignores spectators
                            continue
                        }

                        if (pl.isSpotted) {
                            if (pl.teamNumber == 2) {
                                // terrorist, add to list of spots made by ct
                                for (let c = 0; c < spottedListCTtemp.length; c++) {
                                    if (spottedListCTtemp[c][1] === pl.placeName) {
                                        spottedListCTtemp.splice(c, 1)
                                    }
                                }
                                spottedListCTtemp.push([e, pl.placeName, pl.position])
                            } else {
                                // counter terrorist, add to list of spots made by t
                                for (let c = 0; c < spottedListTtemp.length; c++) {
                                    if (spottedListTtemp[c][1] === pl.placeName) {
                                        spottedListTtemp.splice(c, 1)
                                    }
                                }
                                spottedListTtemp.push([e, pl.placeName, pl.position])
                            }
                        }
                    }

                    // merges duplicate spots
                    for (let newSpot of spottedListCTtemp) {
                        for (let c = spottedListCT.length - 1; c >= 0; c--) {
                            if ((newSpot[0] - spottedListCT[c][0]) < 257) {
                                // duplicate spot less than 4 seconds ago
                                if (spottedListCT[c][1] == newSpot[1]) {
                                    spottedListCT.splice(c, 1)
                                }
                            } else {
                                break
                            }
                        }
                    }
                    spottedListCT.push(...spottedListCTtemp)
                    spottedListCTtemp = []
                    for (let newSpot of spottedListTtemp) {
                        for (let c = spottedListT.length - 1; c >= 0; c--) {
                            if (newSpot[0] - spottedListT[c][0] < 257) {
                                if (spottedListT[c][1] === newSpot[1]) {
                                    spottedListT.splice(c, 1)
                                }
                            } else {
                                break
                            }
                        }
                    }
                    spottedListT.push(...spottedListTtemp)
                    spottedListTtemp = []

                    for (let x = 0; x < demo_file.entities.players.length; x++) {
                        let pl = demo_file.entities.players[x]
                        if (pl.steam64Id == 0) {
                            continue
                        }
                        if (pl.teamNumber == 0 || pl.teamNumber == 1) {
                            continue
                        }
                        let outputdata = `tick${e}\n${pl.position.x},${pl.position.y},${pl.position.z}\n${pl.eyeAngles.pitch},${pl.eyeAngles.yaw}\n`
                        if (pl.teamNumber == 2) {
                            // terrorist
                            outputdata += `spotted${spottedListT.length}\n`
                            if (bombplant) {
                                // holding
                                outputdata += "hold1\n"
                            } else {
                                // not holding
                                outputdata += "hold0\n"
                            }
                            for (let spot of spottedListT) {
                                outputdata += '' + spot[2].x + "," + spot[2].y + "," + spot[2].z + "," + spot[0] + "\n"
                            }
                        } else {
                            // ct
                            outputdata += `spotted${spottedListCT.length}\n`
                            if (bombplant) {
                                // not holding
                                outputdata += "hold0\n"
                            } else {
                                // holding
                                outputdata += "hold1\n"
                            }
                            for (let spot of spottedListCT) {
                                outputdata += '' + spot[2].x + "," + spot[2].y + "," + spot[2].z + "," + spot[0] + "\n"
                            }
                        }

                        fs.appendFile(`./results/${fname},results/${fname},${pl.steam64Id},${kds[pl.steam64Id]}`, outputdata, function (err) {
                            if (err) {
                                fs.writeFile(`./results/${fname},results/${fname},${pl.steam64Id},${kds[pl.steam64Id]}`, outputdata, function (err) {
                                    if (err) throw err;
                                })
                            }
                        })
                    }

                }


                if (roundend) { // resets variables for the list of spotted players
                    spottedListCT = [], spottedListT = []
                }

            })
            demo_file.parse(buffer) // continues parsing
        })
    })
})