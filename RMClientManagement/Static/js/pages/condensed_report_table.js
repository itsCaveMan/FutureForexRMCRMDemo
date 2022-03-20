// ============  STOCK  ============
var stocks = new Stocks('NXH2R828IC9P9FUC')



// ======  ROW OBJECT  ======
class StockRow {

  constructor(DOM_table_row) {
    // this.stockName = stockName;
    this.jTableRow = $(DOM_table_row) // the row in the condensed table, wrapped in $ jquery
    this.fetchStockAPIAttempts = 0
  }

  static MAXIMUM_STOCK_API_FETCH_ATTEMPTS = 10
  static alreadyFetchedStockPrices = {}

  initialize() {
    this.get_variables_from_row();

    this.populate_row();
  }

  get_variables_from_row() {

    this.stockName = this.jTableRow.find('[td_stock_name]').attr('stock_name')

    var openHoldings = this.jTableRow.find('[open_holdings]').attr('open_holdings')
    try {
      openHoldings = parseFloat(openHoldings)
    } catch (e) {
        openHoldings = 0
    }
    this.openHoldings = openHoldings
  }


  async populate_row() {

    // get stock price
    var success = false
    var results = null
    while (success == false & this.fetchStockAPIAttempts < StockRow.MAXIMUM_STOCK_API_FETCH_ATTEMPTS){
      console.log('try get stocks');
      this.fetchStockAPIAttempts += 1
      results = await this.get_current_price_for_stock(this.stockName)
      if (results != false) success = true
    }

    if (success == false) return // if we failed to get the stock api, dont continue

    this.stockAPIResults = results

    this.insert_into_row__stock_price()
    this.insert_into_row__total_net_worth()
    this.insert_into_row__gain_loss()

  }



  async get_current_price_for_stock(stockName) {

    var results = [{
      "open": 0,
      "high": 0,
      "low": 0,
      "close": 0,
      "volume": 0,
      "date": "2000-01-01T00:00:00.000Z"
    }]
    // console.trace();

    try {

      var results = await stocks.timeSeries({
        symbol: stockName,
        interval: '1min',
        amount: 1,
        // start: new Date('2017-07-01'),
        // end: new Date('2017-07-09'),
      });
      console.log({
        results
      });
      console.log(JSON.stringify(results));
      StockRow.alreadyFetchedStockPrices[stockName] = results[0]

    } catch (e) {
      return false
    } finally {
      return results
    }

    // get price

    // store

  }


  insert_into_row__stock_price() {
    // var foo = this.jTableRow.find('[stock_price]')
    // foo.text('A')
    // foo.remove()
    // console.log(foo);
    // console.log(this.stockAPIResults);
    var txt = this.stockAPIResults
    this.jTableRow.find('[stock_price]').text(txt[0]['open'])
  }

  insert_into_row__total_net_worth() {

    if (this.openHoldings == 0) return  // do not try process this column if there are 0 open holdings

    var holdings = parseFloat(this.openHoldings)

    var worth = holdings * this.stockAPIResults[0]['open']

    this.jTableRow.find('[total_net_worth]').text(worth)
    this.marketValue_currentTotalWorth = worth
  }


  insert_into_row__gain_loss() {

    if (this.openHoldings == 0) return  // do not try process this column if there are 0 open holdings

    var gain_loss = this.calculate_gain_loss()
    console.log(gain_loss);
    this.jTableRow.find('[gain_loss__dollars]').text(gain_loss['gain_loss__dollars'])
    this.jTableRow.find('[gain_loss__percentage]').text(gain_loss['gain_loss__percentage'] + '%')
  }



  calculate_gain_loss(numberOfShares, currentPrice) {

    // this.openHoldings

    // var price_payed = this.jTableRow.find('[average_base_cost]').text()
    // var bought_at = parseFloat(price_payed)
    // this.average_price_payed = bought_at

    // var difference = this.openHoldings * price_payed // TODO find this formula from dashbaord

    // now = this.stockAPIResults[0]['open'] // get the stock price now


    // what is the difference between what I HAVE PAID and how much it is WORTH NOW?
    var costBases = this.jTableRow.find('[average_base_cost]').attr('average_base_cost')
    costBases = parseFloat(costBases) // how much i have paid

    var holdings = parseFloat(this.openHoldings)
    var totalWorth = (holdings * costBases)

    var dif =  this.marketValue_currentTotalWorth - totalWorth
    // (+) $4800(worth now) - $4500(ive paid)  = $300
    // (-) $4800(worth now) - $5000(ive paid)  = -$200

    var gain_loss__dollars = dif // $300 = +300
    gain_loss__dollars = Number(gain_loss__dollars).toFixed(2);         // 604.00000000004 --> 604.00

    var gain_loss__percentage = 0

    // get the percentage % of change (% of increase/decrease) by this formula
    gain_loss__percentage = 0
    if (Math.round(totalWorth) > 0){
      gain_loss__percentage = (dif / totalWorth) * 100
    }
    else{
      gain_loss__percentage = "-"
    }

    return {
      "gain_loss__dollars": gain_loss__dollars,
      "gain_loss__percentage": gain_loss__percentage,
    }



  }


}




// ======  ON INIT  ======

$(function() {
  initialize();
});


var allStockRows = []

function initialize() {

  // get every row
  $('[stock_row]').each((i, DOM_e) => {

    row = new StockRow(DOM_e)

    allStockRows.push(row)
  });


  allStockRows.forEach((stockRow, i) => {
    stockRow.initialize()
  });


  // create list of row objects

  // get stock data for each row

  // populate each rows info when data is returned

}









//
//
// async function get_symbol_ticker (stock_symbol) {
//
//   // results = [{'open': 0},]
//
// }
//
//
// async function update_all_symbols_on_page() {
//
//
//   p =  $('[performance]')
//
//   for(var i = 0; i < p.length; i++){
//
//     results = await get_symbol_ticker(symbol)
//
//   }
//
// }
// $(function(){
//     update_all_symbols_on_page()
// });