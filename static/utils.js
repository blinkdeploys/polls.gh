function getColumnTotal(name) {
    const doms = document.getElementsByName(name)
    const totalDoms = document.getElementsByName(`total-${name}`)
    let total = 0
    doms.forEach(function(dom) {
      total += Number(dom.innerHTML)
    })
    totalDoms.forEach(function(totalDom) {
      totalDom.innerHTML = total
    })
}
  
function calculatePercentages() {
    console.log("Winning!")
    const doms = document.getElementsByName('percentage')
    const voteDoms = document.getElementsByName('total-votes')
    const totalDoms = document.getElementsByName(`total-total-votes`)
    const totalVotes = Number(totalDoms[0].innerHTML) || 0
    const totalPercentageDoms = document.getElementsByName('total-percentage')
    let totalPercentage = 0
    if (totalVotes > 0) {
      doms.forEach(function(dom, d) {
        if (voteDoms[d]) {
          const cellValue = Number(voteDoms[d].getAttribute('data-value'))
          const rowPercentage = 100 * cellValue / totalVotes
          dom.innerHTML = rowPercentage
          totalPercentage += rowPercentage
        }
      })
    }
    totalPercentageDoms.forEach(function(totalPercentageDom) {
        totalPercentageDom.innerHTML = totalPercentage
    })
}

function calculateTotals() {
    const BASE_NAME = 'sum-columns'
    const columnHeaders = document.getElementsByName(BASE_NAME)
    columnHeaders.forEach(function(col, c) {
      const colName = col.getAttribute('data-target')
      const cellsInCol = document.querySelectorAll(`[data-col=${colName}]`)
      const totalCol = document.getElementById(`total-${colName}`)
      let total = 0
      cellsInCol.forEach(function(cell) {
        let count = Number(cell.innerHTML) || 0
        total += count
      })
      if (totalCol) {
        totalCol.innerHTML = total
      }
    })
}
  