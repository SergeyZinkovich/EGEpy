from ...GenBase import SingleChoice
from ...Bin import Bin
from ...Bits import Bits
from ...Russian.NumText import num_text
from ...Russian.Names import Names as RussianNames


class Names(SingleChoice):
    def make_condition(self):
        return {'n': self.rnd.in_range(1, 5),
                'type' : (1 if self.rnd.in_range(1, 6) > 1 else 2),
                'vc' : self.rnd.coin()
                }

    def cond_to_text(self, cond):
        pos_names = ['Первая', 'Вторая', 'Третья', 'Четвёртая', 'Пятая', 'Шестая']
        count_names = ['одна', 'две', 'три', 'четыре', 'пять', 'шесть']
        letters = ['гласная буква', 'гласных буквы', 'гласных букв']

        vc = 'со' if cond['vc'] else ''
        if cond['type'] == 1:
            pos_names[cond['n'] - 1] + " буква ${vc}гласная"
        else:
            'В слове ' + num_text(cond['n'], [map "$vc$_", @ letters])

    def make_cond_group(self):
        g = {'size': self.rnd.pick(2, 3)}
        v = g['vars'] = [0 for _ in range(g['size'])]
        g['expr'] = EGE::Logic::random_logic_expr(map \$_,@$v);
        c = g['cond'] = [make_condition]
        for (2.. $g->{size}) {
            my $new_cond;
        do {
        $new_cond = make_condition;
        }
        while grep cond_eq($_, $new_cond), @ $c;
        push @$c, $new_cond;

    }
    $v->[$_] = cond_to_text($c->[$_]) for 0.. $g->{size} - 1;
    $g->{text} = $g->{expr}->to_lang_named('Logic');
    $g->{min_len} = List::
        Util::max(map $_->{n},@$c);
        return g

    def check_cond_group(self, g, s):
        $g->{vars}->[$_] = check_cond($g->{cond}->[$_], $s)
        for 0.. $g->{size} - 1;

    $g->{expr}->run({}) ? 1: 0;

    def strings(self, init_string, next_string, list_text):
        good = -1
        do
        {
        g = make_cond_group()
        true_false = [[], []]
        $init_string->()
        while (s = $next_string->()) {
            next if len(s) < $g->{min_len};
            push @ {$true_false->[check_cond_group($g, $str)]}, $s
            good = check_good(true_false)
        } while $good < 0
        tf = 'истинно' if good != 0  else 'ложно'

        self.text = f'Для какого {$list_text} {$tf} высказывание:<br/>{$g->text}?'
        self.set_variants($true_false->[$good][0],@{$true_false->[1 - $good]}[0.. 2]);

    def generate(self):
        l = self.rnd.shuffle(RussianNames.all_names)
        i = 0
        self.strings(sub{ $i = 0}, sub{ $list[$i + +]}, 'имени')
