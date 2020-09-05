from django.core.exceptions import ValidationError
acceptable_characters = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

def color(value):
    if len(value) < 6:
        raise ValidationError('This string must have length equal to 6.')
        return

    all_ok = True
    for s in value:
        ok = False
        for char in acceptable_characters:
            if char == s:
                ok = True
                break
        if not ok:
            all_ok = False
            break

    if not all_ok:
        raise ValidationError('This string must consist of these characters only: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F.')