$(".modify").click(function () {
    $(this).parent().siblings("td").each(function () //找同类元素td
        {
            var is_text = $(this).find("input:text"); //判断单元格下是否含有文本框
            if (!is_text.length) {
                $(this).html("<input size='13' type='text' value=' " + $(this).text() + " ' />");
            } else
                $(this).html(is_text.val());
        })
});

$(".remove").click(function () {
    if (window.confirm("您确定要删除数据吗?")) {
        $(this).parent().parent().remove();
    }
});