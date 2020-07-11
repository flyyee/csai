const fs = require("fs");
const demofile = require("demofile");

function clog(text) {
    console.log(text)
}

fs.readdir("./newd", (err, files) => {
    if (err) throw err
    files.forEach(file => {
        console.log(`${file} is beginning parsing`)


        let spottedlist = {}
        let kds = {}
        let spotted = []
        let samespot = false
        let matchstart = false, roundstart = false, roundend = false, bombplant = false
        let timecount = 0, showtick = false, stillrunning = true

        // const fname = "singularity-vs-saw-m3-dust2"
        const fname = file.substr(0, file.length - 4)

        if (!fs.existsSync(`./rez/${fname},results`)) {
            fs.mkdirSync(`./rez/${fname},results`);
        }

        fs.readFile(`./newd/${fname}.dem`, (err, buffer) => {
            const demo_file = new demofile.DemoFile()

            demo_file.gameEvents.on("round_announce_match_start", e => {
                matchstart = true
                clog("match start")
                var interval = setInterval(function () {
                    timecount++
                    console.log(`${timecount}mins elapsed\n`)
                    showtick = true
                    stillrunning = false
                    setTimeout(() => {
                        if (!stillrunning) {
                            clearInterval(interval)
                            console.log(`${fname} has been parsed`)
                        }
                    }, 5000)
                }, 60000)
                // setTimeout(function() { 
                //     clearInterval(interval); 
                // }, 10000);
            })


            demo_file.gameEvents.on("round_start", e => {
                if (matchstart) {
                    // clog("round start")
                    roundstart = true
                    roundend = false
                }
            })

            demo_file.gameEvents.on("round_end", e => {
                if (matchstart) {
                    roundstart = false
                    roundend = true
                    bombplant = false

                    for (let x = 0, y = 0; x < demo_file.entities.players.length; x++) {
                        let pl = demo_file.entities.players[x]
                        if (pl.steam64Id == 0) {
                            continue
                        }
                        if (pl.teamNumber == 0 || pl.teamNumber == 1) {
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
                        if (newkd.length == 1) {
                            newkd = newkd + ".00"
                        } else if (newkd.length == 3) {
                            newkd = newkd + "0"
                        }
                        newkd = newkd.replace(".", ",")
                        fs.rename(`./rez/${fname},results/${fname},${pl.steam64Id},${kds[pl.steam64Id]}`, `./rez/${fname},results/${fname},${pl.steam64Id},${newkd}`, (err) => {
                            // console.log(err)
                        })
                        kds[pl.steam64Id] = newkd
                    }

                }
            })

            demo_file.gameEvents.on("bomb_planted", e => {
                if (matchstart) {
                    bombplant = true
                }
            })

            demo_file.on("tickend", e => {
                // clog(e)
                // if (e > 1000) {
                if (showtick) {
                    clog(e)
                    showtick = false
                    stillrunning = true
                }
                if (roundstart) {
                    for (let x = 0, y = 0; x < demo_file.entities.players.length; x++) {
                        let pl = demo_file.entities.players[x]
                        if (pl.steam64Id == 0) {
                            continue
                        }
                        if (pl.teamNumber == 0 || pl.teamNumber == 1) {
                            continue
                        }
                        if (spottedlist[pl.steam64Id] == undefined) {
                            spottedlist[pl.steam64Id] = []
                        }
                        // clog(pl.position)
                        // clog(pl.eyeAngles)
                        // clog(pl.allSpotted)
                        for (let spot of pl.allSpotted) {
                            samespot = false
                            for (let player of demo_file.entities.players) {
                                if (player.steam64Id === spot.steam64Id) {
                                    for (let prevspot of spotted) {
                                        if (prevspot[0] === e - 1) {
                                            if (prevspot[1] === player.steam64Id) {
                                                samespot = true
                                            }
                                        }
                                    }
                                    if (!samespot) {
                                        spottedlist[pl.steam64Id].push([e, player.steam64Id, player.position])
                                    }
                                    break
                                }
                            }
                        }
                        // clog("spottedlist")
                        // clog(x)
                        // clog(spottedlist)
                        let outputdata = `tick${e}\n${pl.position.x},${pl.position.y},${pl.position.z}\n${pl.eyeAngles.pitch},${pl.eyeAngles.yaw}\nspotted${spottedlist[pl.steam64Id].length}\n`
                        if (pl.teamNumber == 2) {
                            if (bombplant) {
                                outputdata += "hold1\n"
                            } else {
                                outputdata += "hold0\n"
                            }
                        } else {
                            if (bombplant) {
                                //nohold
                                outputdata += "hold0\n"
                            } else {
                                //hold
                                outputdata += "hold1\n"
                            }
                        }
                        for (let sp of spottedlist[pl.steam64Id]) {
                            outputdata += '' + sp[2].x + "," + sp[2].y + "," + sp[2].z + "," + sp[0] + "\n"
                        }
                        fs.appendFile(`./rez/${fname},results/${fname},${pl.steam64Id},${kds[pl.steam64Id]}`, outputdata, function (err) {
                            if (err) {
                                fs.writeFile(`./rez/${fname},results/${fname},${pl.steam64Id},${kds[pl.steam64Id]}`, outputdata, function (err) {
                                    if (err) throw err;
                                })
                            }
                        })
                    }
                }


                if (roundend) {
                    spottedlist = {}
                }

            })
            demo_file.parse(buffer)
        })
    })
})

// let spottedlist = {}
// let kds = {}
// let spotted = []
// let samespot = false
// let matchstart = false, roundstart = false, roundend = false, bombplant = false
// let timecount = 0, showtick = false, stillrunning = true

// const fname = "singularity-vs-saw-m3-dust2"

// if (!fs.existsSync(`./${fname},results`)){
//     fs.mkdirSync(`./${fname},results`);
// }

// fs.readFile(`${fname}.dem`, (err, buffer) => {
//     const demo_file = new demofile.DemoFile()

//     demo_file.gameEvents.on("round_announce_match_start", e => {
//         matchstart = true
//         clog("match start")
//         var interval = setInterval(function(){
//             timecount++
//             console.log(`${timecount}mins elapsed\n`)
//             showtick = true
//             stillrunning = false
//             setTimeout(() => {
//                 if (!stillrunning) {
//                     clearInterval(interval)
//                     console.log(`${fname} has been parsed`)
//                 }
//             }, 5000)
//           }, 60000)
//         // setTimeout(function() { 
//         //     clearInterval(interval); 
//         // }, 10000);
//     })


//     demo_file.gameEvents.on("round_start", e => {
//         if (matchstart) {
//             // clog("round start")
//             roundstart = true
//             roundend = false
//         }
//     })

//     demo_file.gameEvents.on("round_end", e => {
//         if (matchstart) {
//             roundstart = false
//             roundend = true
//             bombplant = false

//             for (let x = 0, y = 0; x < demo_file.entities.players.length; x++) {
//                 let pl = demo_file.entities.players[x]
//                 if (pl.steam64Id == 0) {
//                     continue
//                 }
//                 if (pl.teamNumber == 0 || pl.teamNumber == 1) {
//                     continue
//                 }
//                 let newkd
//                 if (pl.kills == 0) {
//                     newkd = 0
//                 } else if (pl.deaths == 0) {
//                     newkd = pl.kills + 1
//                 } else {
//                     newkd = Math.round(pl.kills / pl.deaths * 100)/100
//                 }
//                 newkd = String(newkd)
//                 if (newkd.length == 1) {
//                     newkd = newkd + ".00"
//                 } else if (newkd.length == 3) {
//                     newkd = newkd + "0"
//                 }
//                 newkd = newkd.replace(".", ",")
//                 fs.rename(`./${fname},results/${fname},${pl.steam64Id},${kds[pl.steam64Id]}`, `./${fname},results/${fname},${pl.steam64Id},${newkd}`, (err) => {
//                     // console.log(err)
//                 })
//                 kds[pl.steam64Id] = newkd
//             }

//         }
//     })

//     demo_file.gameEvents.on("bomb_planted", e => {
//         if (matchstart) {
//             bombplant = true
//         }
//     })

//     demo_file.on("tickend", e => {
//         // clog(e)
//         // if (e > 1000) {
//         if (showtick) {
//             clog(e)
//             showtick = false
//             stillrunning = true
//         }
//         if (roundstart) {
//             for (let x = 0, y = 0; x < demo_file.entities.players.length; x++) {
//                 let pl = demo_file.entities.players[x]
//                 if (pl.steam64Id == 0) {
//                     continue
//                 }
//                 if (pl.teamNumber == 0 || pl.teamNumber == 1) {
//                     continue
//                 }
//                 if (spottedlist[pl.steam64Id] == undefined) {
//                     spottedlist[pl.steam64Id] = []
//                 }
//                 // clog(pl.position)
//                 // clog(pl.eyeAngles)
//                 // clog(pl.allSpotted)
//                 for (let spot of pl.allSpotted) {
//                     samespot = false
//                     for (let player of demo_file.entities.players) {
//                         if (player.steam64Id === spot.steam64Id) {
//                             for (let prevspot of spotted) {
//                                 if (prevspot[0] === e-1) {
//                                     if (prevspot[1] === player.steam64Id) {
//                                         samespot = true
//                                     }
//                                 }
//                             }
//                             if (!samespot) {
//                                 spottedlist[pl.steam64Id].push([e, player.steam64Id, player.position])
//                             }
//                             break
//                         }
//                     }
//                 }
//                 // clog("spottedlist")
//                 // clog(x)
//                 // clog(spottedlist)
//                 let outputdata = `tick${e}\n${pl.position.x},${pl.position.y},${pl.position.z}\n${pl.eyeAngles.pitch},${pl.eyeAngles.yaw}\nspotted${spottedlist[pl.steam64Id].length}\n`
//                 if (pl.teamNumber == 2) {
//                     if (bombplant) {
//                         outputdata += "hold1\n"
//                     } else {
//                         outputdata += "hold0\n"
//                     }
//                 } else {
//                     if (bombplant) {
//                         //nohold
//                         outputdata += "hold0\n"
//                     } else {
//                         //hold
//                         outputdata += "hold1\n"
//                     }
//                 }
//                 for (let sp of spottedlist[pl.steam64Id]) {
//                     outputdata += ''+sp[2].x+","+sp[2].y+","+sp[2].z+","+sp[0]+"\n"
//                 }
//                 fs.appendFile(`./${fname},results/${fname},${pl.steam64Id},${kds[pl.steam64Id]}`, outputdata, function (err) {
//                     if (err) {
//                         fs.writeFile(`./${fname},results/${fname},${pl.steam64Id},${kds[pl.steam64Id]}`, outputdata, function (err) {
//                             if (err) throw err;
//                         })
//                     }
//                 })
//             }
//         }


//         if (roundend) {
//             spottedlist = {}
//         }

//     })
//     demo_file.parse(buffer)
// })