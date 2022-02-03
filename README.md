# Misc-Scripts
Miscellaneous Scripts I use for work.

# RegionReplace.py
This is meant to be run as a Git pre-commit hook to replace specified regions in your M.U.G.E.N CNS scripts when you have common system files. This assumes you have a
subrepo in your character with common system files.

## Installation
Replace the contents of your system repo's git hooks `pre-commit` file (located in `.git/hooks`) with the contents of RegionReplace.py, set up your `directories`, 
`subdirectories`, and `copyFiles` variables, and then save.

## Usage
Suppose your project has the following structure:
```
    /char
	|
    |_char.def
    |_char.cns
    |_char.cds
    |_char.sff
    |_char.snd
    |____/overrides
    |    |
    |    |_first_attack_triggers.cns
	|
    |____/system
        |
        |_/.git
          |
          |____/hooks
               |
               |_pre-commit
```

And suppose in `char.cns` under `[StateDef -2]` there is following CNS snippet:

```ini
[State 180, 1]
type = VarSet
triggerall = Var(21)
triggerall = p2movetype = H
trigger1 = (stateno != [800,899])
trigger1 = movehit
trigger2 = projhit = 1
;#region first_attack_triggers.cns
;#endregion
fvar(32) = 1
ignorehitpause = 1
```

.. and the contents of `first_attack_triggers.cns` are as follows:
```ini
trigger3 = (stateno = [810,815]) && anim = 806 && animelem = 3 && movetype != H
trigger4 = stateno = 831 && animelem = 14 && movetype != H
trigger5 = stateno = 832 && animelem = 14 && movetype != H
trigger6 = stateno = 1501 && anim = 1500 && animelem = 4 && movetype != H
trigger7 = NumHelper(3103)
trigger7 = Helper(3103), MoveHit
trigger8 = NumHelper(3106)
trigger8 = Helper(3106), MoveHit
trigger9 = NumHelper(1105)
trigger9 = Helper(1105), MoveHit
```

Then when you run `git commit` on your `system` repo, assuming you have your configuration set up to look in the character folder (default behavior), the region in your
`char.cns` will be replaced with the contents in `override/first_attack_triggers.cns`, leading to the following result:

```ini
[State 180, 1]
type = VarSet
triggerall = Var(21)
triggerall = p2movetype = H
trigger1 = (stateno != [800,899])
trigger1 = movehit
trigger2 = projhit = 1
;#region first_attack_triggers.cns
trigger3 = (stateno = [810,815]) && anim = 806 && animelem = 3 && movetype != H
trigger4 = stateno = 831 && animelem = 14 && movetype != H
trigger5 = stateno = 832 && animelem = 14 && movetype != H
trigger6 = stateno = 1501 && anim = 1500 && animelem = 4 && movetype != H
trigger7 = NumHelper(3103)
trigger7 = Helper(3103), MoveHit
trigger8 = NumHelper(3106)
trigger8 = Helper(3106), MoveHit
trigger9 = NumHelper(1105)
trigger9 = Helper(1105), MoveHit
;#endregion
fvar(32) = 1
ignorehitpause = 1
```

... pretty simple, no? Regions within regions are also supported; the contents of inner regions are recursively replaced.