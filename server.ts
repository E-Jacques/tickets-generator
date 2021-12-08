import * as express from "express";
import { Request, Response } from "express";
import { readFileSync } from "fs";

let allHashList: string[] = []
let usedHashList: string[] = []

const app = express()
app.set("view engine", "ejs")

loadData("./hash.txt")

app.get("/:hash", getHashAviability)
app.post("/:hash", useHash)

function loadData(hashPath: string) {
    let data = readFileSync(hashPath, { encoding: "ascii" })
    let lines = data.split("\n")
    for (let line of lines) {
        if (line) {
            allHashList.push(line)
        }
    }
}

function useHash (req: Request, res: Response) {
    let hash = req.params.hash

    if (allHashList.includes(hash) && !usedHashList.includes(hash)) {
        console.log("use");
        
        usedHashList.push(hash)
    }

    return res.render("index", {
        hash: hash,
        avaibility: "Déjà utilisé ...",
        title: "Marché de Noel !"
    })
}

function getHashAviability(req: Request, res: Response) {
    let hash = req.params.hash
    let o = {
        hash: hash,
        avaibility: "Utilisable !",
        title: "Marché de Noel !"
    }

    if (allHashList.includes(hash) && !usedHashList.includes(hash)) {
        return res.render("index", o)
    }

    o.avaibility = "Déjà utilisé ..."
    return res.render("index", o)
}

app.listen(3000, () => {
    console.log("Server online on port 3000")
})