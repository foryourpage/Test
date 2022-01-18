(function ($) {
  $.fn.FontScroll = function (options) {
    let d = { time: 1000 }
    $.extend(d, options);

    // 需要滚动的div父盒子
    let box = this[0]
    // 滚动间隔
    let _time = d.time

    // 这个办法只适合每行数据的高度都相同的情况
    // // 每次滚动的高度（一般是一条数据的高度）
    // let _contentChildHeight = box.children[0].children[0].offsetHeight
    // // 滚动总高度，即内容的总高度（所有数据的总高度）
    // let _contentTotalHeight = _contentChildHeight * box.children[0].children.length

    // 这种办法适合所有情况，包括每行数据的高度都不相同的情况
    // 获取所有行元素
    let all_row_el = box.children[0].children
    // 行总高度
    let _contentTotalHeight = 0
    // 每一行数据与前面所有行高度的叠加高度
    let _contentChildHeight = []
    for (let i in all_row_el) {
      if ((new RegExp("^\\d+$")).test(i)) {
        _itemHeight = all_row_el[i].offsetHeight
        _contentTotalHeight += _itemHeight
        i == 0 ? _contentChildHeight.push(_itemHeight) : _contentChildHeight.push(_contentChildHeight[i - 1] + _itemHeight)
      }
    }

    // 需要滚动的div子盒子
    let child1 = this.children('.box-body')
    // 克隆出来滚动的div子盒子
    // 克隆方法一
    // let child1 = this.children('.box-body')[0]
    // let child2 = this.children('.box-body')[1]
    // child2.innerHTML = child1.innerHTML
    // 克隆方法二
    if ((box.offsetHeight + 5) < _contentTotalHeight) {
      // 如果数据没有达到一定的高度，则不会执行滚动效果
      child1.clone().insertAfter(child1)
      /*启动定时器*/
      let timer = setInterval(autoScrollLine, 30)
      /*单行向上滚动效果*/
      function autoScrollLine() {
        /*判断滚动内容是否已经滚完，滚完了则滚动的值重新设置到0
        否则就每隔30毫秒向上滚动1px*/
        if (box.scrollTop >= _contentTotalHeight) {
          box.scrollTop = 0;
        } else {
          box.scrollTop++;
        }
        /*判断滚动的距离刚好为一条數據的高度时停掉定时器，
        隔 _time 之后重新启动定时器即可实现數據滚动停留效果 */
        if (_contentChildHeight.indexOf(box.scrollTop) >= 0) {
          clearInterval(timer)
          setTimeout(() => {
            timer = setInterval(autoScrollLine, 30)
          }, _time)
        }
      }
    }
  }
})(jQuery);

