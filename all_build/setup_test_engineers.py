from common.views import add_test_user
from register.models import Engineer

Engineer.objects.all().delete()
add_test_user('James', 'Way', 'Fire Management Scotland', '21 Baker Ave', 'New Way', 'Lochardil', 'IV2 3NK', 'Inverness', 0, 0, 2)
add_test_user('Adam', 'Bitten', 'Direct Line', '2a Hunters Place', '', '', 'PA16 7TB', 'Greenock', 0, 1, 0)
add_test_user('Michelle', 'Lourdes', 'Halpway Ext', '207 Halford Way', '', '', 'AV2 8FF', 'Aviemore', 2, 2, 1)
add_test_user('Andy', 'Match', 'Big Help', '12 Mary Bourne House', 'Kelpie', '', 'KP 9A', 'Aberdeen', 1, 3, 4)
add_test_user('Kyle', 'McIntyre', 'Charcoal', 'Alexander Place', '', '', 'PA19 3E', 'Paisley', 1, 4, 1)
add_test_user('Dwayne', 'Gunn', 'Low Budge', '109 Ruth St', '', '', 'A129 9', 'Arran', 1, 2, 4)

