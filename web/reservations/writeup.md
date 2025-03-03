`OR` is one of the last keywords to be checked, so we can hide it in other keywords, so that those keywords appear when the `OR` is removed, such as `selecORt` turning into `select`.

The payload `' unioORn selecORt *, nulORl froORm users;/*` works to get the flag, turning into `' union select *, null from users;/*` after the filtering is applied.