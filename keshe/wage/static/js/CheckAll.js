            //全选或全不选
            function selectAll() {
                var items = document.getElementsByName("checkItem");
                var checkAll = document.getElementById("checkAll");
                var checkOther = document.getElementById("checkOther");
                checkOther.checked = false;
                for (var i = 0; i < items.length; i++) {
                    items[i].checked = checkAll.checked;
                }
            }
            //反选
            function selectOther() {
                var items = document.getElementsByName("checkItem");
                var checkAll = document.getElementById("checkAll");
                var checkOther = document.getElementById("checkOther");
                checkAll.checked = false;
                for (var i = 0; i < items.length; i++) {
                    items[i].checked = !items[i].checked;
                }
            }


            A