sym_layer = """
        &kp GB_TILDE  &kp PLUS            &kp MINUS                      &kp PERCENT         &kp GB_DOLLAR                  &kp GB_POUND_SIGN                   &kp GB_AT_SIGN  &HT_Double_Pipe 0 GB_PIPE  &kp CARET  &trans
        &trans        &kp LBRC            &kp STAR                       &kp RBRC            &HT_Double_Bslash 0 GB_BSLH    &HT_Triple_Apostrophe 0 GRAVE       &kp LPAR        &kp QMARK                  &kp RPAR   &HT_Double_Hash 0 GB_HASH
&trans  &trans        &HT_Double_LT 0 LT  &HT_Double_Bang 0 EXCLAMATION  &HT_Double_GT 0 GT  &trans                         &HT_Double_Underscore 0 UNDERSCORE  &kp LBKT        &kp AMPS                   &kp RBKT   &trans                     &trans
"""
num_layer = """
        &trans  &kp PLUS  &kp MINUS  &kp PERCENT  &trans    &trans  &kp AT  &trans  &trans  &trans
        &kp N6  &kp N4    &kp N0     &kp N2       &trans    &trans  &kp N3  &kp N1  &kp N5  &kp N7
&trans  &trans  &trans    &trans     &kp N8       &trans    &trans  &kp N9  &kp J   &kp K   &trans  &trans
"""


def parse_layer(layer):
    rows = layer.split("\n")
    i = 0
    bindings = {}

    for l in rows:
        l = l.strip()
        if not l:
            continue
        bind = [k.strip() for k in l.split("&") if k.strip()]
        if not bind:
            continue
        for b in bind:
            if b != "trans":
                bindings[i] = "&" + b
            i += 1

    return bindings


# #define THUMB_COMBO(NAME, THUMB_POS, KEY_POS, BINDING) \
# combo_##NAME : NAME { \
#     timeout-ms = <30>; \
#     key-positions = <THUMB_POS KEY_POS>; \
#     bindings = <BINDING>; \
# };
def combo(name, thumb_pos, key_pos, binding):
    return f"""        combo_{name} {{
            bindings = <{binding}>;
            key-positions = <{thumb_pos} {key_pos}>;
        }};
"""


sym_bindings = parse_layer(sym_layer)
num_bindings = parse_layer(num_layer)

print("Symbol Bindings:", sym_bindings)
print("Number Bindings:", num_bindings)

l_keys = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 25]
r_keys = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 26, 27, 28, 29, 30, 31]

output = []

# same side = symbol
for lkey in l_keys:
    if lkey in sym_bindings:
        output.append(
            # f"THUMB_COMBO(l_sym_{lkey}, L_THUMB, {lkey}, {sym_bindings[lkey]})"
            combo(f"l_sym_{lkey}", 33, lkey, sym_bindings[lkey])
        )
output.append("\n")

for lkey in l_keys:
    if lkey in num_bindings:
        output.append(
            # f"THUMB_COMBO(r_num_{lkey}, R_THUMB, {lkey}, {num_bindings[lkey]})"
            combo(f"l_num_{lkey}", 36, lkey, num_bindings[lkey])
        )
output.append("\n")

for rkey in r_keys:
    if rkey in sym_bindings:
        output.append(
            # f"THUMB_COMBO(r_sym_{rkey}, R_THUMB, {rkey}, {sym_bindings[rkey]})"
            combo(f"r_sym_{rkey}", 36, rkey, sym_bindings[rkey])
        )

output.append("\n")
for rkey in r_keys:
    if rkey in num_bindings:
        output.append(
            # f"THUMB_COMBO(l_num_{rkey}, L_THUMB, {rkey}, {num_bindings[rkey]})"
            combo(f"r_num_{rkey}", 33, rkey, num_bindings[rkey])
        )

with open("key_combos.dtsi", "w") as f:
    f.write("\n".join(output))
