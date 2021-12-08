import * as express from "express";
import { Request, Response } from "express";
import { readFileSync } from "fs";

let allHashList: string[] = []
let usedHashList: string[] = []

const app = express()
loadData("./hash.txt")

app.get("/:hash", getHashAviability)

function loadData(hashPath: string) {
    let data = readFileSync(hashPath, { encoding: "ascii" })
    let lines = data.split("\n")
    for (let line of lines) {
        if (line) {
            allHashList.push(line)
        }
    }
}

function getHashAviability(req: Request, res: Response) {
    let hash = req.params.hash

    if (allHashList.includes(hash) && !usedHashList.includes(hash)) {
        usedHashList.push(hash)
        return res.send("Avaible")
    }

    return res.send("Already used")
}

app.listen(3000, () => {
    console.log("Server online on port 3000")
})