import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";

const TalentScaling = {
  1: [44.5, 43.7, 54.9, 58.4, 73.9, 87.3, 103.0],
  2: [47.6, 46.7, 58.7, 62.5, 79.1, 93.4, 110.2],
  3: [51.6, 50.6, 63.7, 67.9, 85.9, 101.4, 119.7],
  4: [56.3, 55.3, 69.7, 74.3, 94.0, 110.9, 131.0],
  5: [59.4, 58.3, 73.5, 78.4, 99.2, 117.0, 138.2],
  6: [62.9, 61.7, 77.8, 83.0, 105.1, 124.0, 146.4],
  7: [68.5, 67.2, 84.8, 90.4, 114.5, 135.1, 159.5],
  8: [74.1, 72.8, 91.8, 97.8, 124.0, 146.3, 172.6],
  9: [79.8, 78.3, 98.9, 105.2, 133.4, 157.4, 185.7],
  10: [85.9, 84.3, 106.5, 113.3, 143.8, 169.6, 199.9],
};

function calculateDamage(baseATK, multiplier, bonusDMG, critRate, critDMG, shred, resMult) {
  const totalMultiplier = multiplier * (1 + bonusDMG + shred) * resMult;
  const nonCrit = baseATK * totalMultiplier / 100;
  const crit = nonCrit * (1 + critDMG);
  const avg = (crit * critRate + nonCrit * (1 - critRate));
  return { nonCrit, crit, avg };
}

function calculateReaction(baseDMG, EM, type) {
  const EM_bonus = (2.78 * EM) / (1400 + EM);
  const multiplier = {
    swirl: 1.2,
    vaporize: 1.5,
    melt: 2.0,
    overload: 4.0,
    superconduct: 1.0,
    electrocharged: 1.2,
    burning: 0.25,
    burgeon: 3.0,
    bloom: 2.0,
    hyperbloom: 3.0,
    aggravate: 1.15,
    spread: 1.25,
  }[type] || 1;
  return baseDMG * multiplier * (1 + EM_bonus);
}

export default function GenshinDmgCalc() {
  const [baseATK, setBaseATK] = useState(2000);
  const [bonusDMG, setBonusDMG] = useState(0.466);
  const [critRate, setCritRate] = useState(0.616);
  const [critDMG, setCritDMG] = useState(1.41);
  const [talentLevel, setTalentLevel] = useState("10");
  const [enemyShred, setEnemyShred] = useState(0);
  const [resMult, setResMult] = useState(0.9);
  const [EM, setEM] = useState(100);
  const [reactionType, setReactionType] = useState("swirl");
  const [numAttacks, setNumAttacks] = useState(3);

  const multipliers = TalentScaling[parseInt(talentLevel)].slice(0, numAttacks);

  const results = multipliers.map((multi, i) => {
    const dmg = calculateDamage(baseATK, multi, bonusDMG, critRate, critDMG, enemyShred, resMult);
    const reaction = calculateReaction(dmg.avg, EM, reactionType);
    return { i: i + 1, ...dmg, reaction };
  });

  return (
    <div className="grid gap-4 p-4">
      <Card>
        <CardContent className="grid gap-2">
          <Label>Base ATK</Label>
          <Input type="number" value={baseATK} onChange={e => setBaseATK(+e.target.value)} />

          <Label>% Bonus DMG</Label>
          <Input type="number" step="0.01" value={bonusDMG} onChange={e => setBonusDMG(+e.target.value)} />

          <Label>CRIT Rate</Label>
          <Input type="number" step="0.01" value={critRate} onChange={e => setCritRate(+e.target.value)} />

          <Label>CRIT DMG</Label>
          <Input type="number" step="0.01" value={critDMG} onChange={e => setCritDMG(+e.target.value)} />

          <Label>Talent Level</Label>
          <Select value={talentLevel} onValueChange={setTalentLevel}>
            <SelectTrigger><SelectValue placeholder="Talent Level" /></SelectTrigger>
            <SelectContent>
              {[...Array(10)].map((_, i) => (
                <SelectItem key={i} value={(i + 1).toString()}>{i + 1}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Label>Enemy RES Multiplier</Label>
          <Input type="number" step="0.01" value={resMult} onChange={e => setResMult(+e.target.value)} />

          <Label>Elemental Shred (decimal)</Label>
          <Input type="number" step="0.01" value={enemyShred} onChange={e => setEnemyShred(+e.target.value)} />

          <Label>Elemental Mastery</Label>
          <Input type="number" value={EM} onChange={e => setEM(+e.target.value)} />

          <Label>Tipo Reazione</Label>
          <Select value={reactionType} onValueChange={setReactionType}>
            <SelectTrigger><SelectValue placeholder="Tipo Reazione" /></SelectTrigger>
            <SelectContent>
              {Object.keys({
                swirl: 1, vaporize: 1, melt: 1, overload: 1, superconduct: 1, electrocharged: 1, burning: 1, burgeon: 1, bloom: 1, hyperbloom: 1, aggravate: 1, spread: 1,
              }).map(type => (
                <SelectItem key={type} value={type}>{type}</SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Label>Numero attacchi normali</Label>
          <Select value={numAttacks.toString()} onValueChange={val => setNumAttacks(parseInt(val))}>
            <SelectTrigger><SelectValue placeholder="Numero attacchi" /></SelectTrigger>
            <SelectContent>
              {[...Array(7)].map((_, i) => (
                <SelectItem key={i} value={(i + 1).toString()}>{i + 1}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </CardContent>
      </Card>

      {results.map(({ i, nonCrit, crit, avg, reaction }) => (
        <Card key={i}>
          <CardContent className="p-4">
            <h3 className="font-bold">Attacco Normale {i}</h3>
            <p>Danno Non Critico: {nonCrit.toFixed(1)}</p>
            <p>Danno Critico: {crit.toFixed(1)}</p>
            <p>Danno Medio: {avg.toFixed(1)}</p>
            <p>Danno con Reazione ({reactionType}): {reaction.toFixed(1)}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
