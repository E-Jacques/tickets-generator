"use strict";
exports.__esModule = true;
var express = require("express");
var fs_1 = require("fs");
var allHashList = [];
var usedHashList = [];
var app = express();
app.set("view engine", "ejs");
loadData("./hash.txt");
app.get("/:hash", getHashAviability);
app.post("/:hash", useHash);
function loadData(hashPath) {
    var data = (0, fs_1.readFileSync)(hashPath, { encoding: "ascii" });
    var lines = data.split("\n");
    for (var _i = 0, lines_1 = lines; _i < lines_1.length; _i++) {
        var line = lines_1[_i];
        if (line) {
            allHashList.push(line);
        }
    }
}
function useHash(req, res) {
    var hash = req.params.hash;
    if (allHashList.includes(hash) && !usedHashList.includes(hash)) {
        usedHashList.push(hash);
    }
    return res.render("index", {
        hash: hash,
        avaibility: "Déjà utilisé ...",
        title: "Marché de Noel !"
    });
}
function getHashAviability(req, res) {
    var hash = req.params.hash;
    var o = {
        hash: hash,
        avaibility: "Utilisable !",
        title: "Marché de Noel !"
    };
    if (!allHashList.includes(hash)) {
    o.avaibility = "Inconnu :(";
    return res.render("index", o);
    }
    if (allHashList.includes(hash) && !usedHashList.includes(hash)) {
        return res.render("index", o);
    }
    o.avaibility = "Déjà utilisé ...";
    return res.render("index", o);
}
app.listen(3001, function () {
    console.log("Server online on port 3000");
});
