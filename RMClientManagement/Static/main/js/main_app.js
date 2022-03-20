

var app = angular.module('rmms');

app.controller('mainController', ['$scope', '$window', mainController]);

function mainController($scope, $window) {

  // default values for time selection of new class
  $scope.new_class_time__start_hour     = 9;

  $scope.move_class_order = function (i) {

    // move class to the front of the array
    //https://stackoverflow.com/questions/5306680/move-an-array-element-from-one-array-position-to-another?rq=1
    var element = $scope.classes[i];
    $scope.classes.splice(i, 1);
    $scope.classes.splice(0, 0, element);

  }

  $scope.populate_calendar = function (){

    calendar.clear(true)

    setTimeout(
      ()=>{
        $scope.classes.forEach((_class, i) => {

          if(_class.show_in_schedule == false)
            return


          var new_class =
          {
            id:           _class.id,
            name:         _class.name,          //
            professor:    _class.professor,     //
            days_of_week: _class.days_of_week,
            time_start:   _class.time_start,
            time_end:     _class.time_end,
            bgColor:      _class.bgColor,
            bColor:      _class.bColor,
            // category: _class.category,      // Major/minor/ge...
          }


          var schedule = {
                calendarId: '1',
                title: new_class.name,
                category: 'time',
                color: '#252525a6',
                bgColor: new_class.bgColor,
                borderColor: new_class.bColor
            }

          if(new_class.days_of_week[0] == 1){
            schedule.id     = new_class.id
            schedule.start  = new Date(2091, 0, 1, new_class.time_start[0], new_class.time_start[1], 0, 0)
            schedule.end    = new Date(2091, 0, 1, new_class.time_end[0], new_class.time_end[1], 0, 0)
            calendar.createSchedules([schedule])
          }
          if(new_class.days_of_week[1] == 1){
            schedule.id     = new_class.id
            schedule.start  = new Date(2091, 0, 2, new_class.time_start[0], new_class.time_start[1], 0, 0)
            schedule.end    = new Date(2091, 0, 2, new_class.time_end[0], new_class.time_end[1], 0, 0)
            calendar.createSchedules([schedule])
          }
          if(new_class.days_of_week[2] == 1){
            schedule.id     = new_class.id
            schedule.start  = new Date(2091, 0, 3, new_class.time_start[0], new_class.time_start[1], 0, 0)
            schedule.end    = new Date(2091, 0, 3, new_class.time_end[0], new_class.time_end[1], 0, 0)
            calendar.createSchedules([schedule])
          }
          if(new_class.days_of_week[3] == 1){
            schedule.id     = new_class.id
            schedule.start  = new Date(2091, 0, 4, new_class.time_start[0], new_class.time_start[1], 0, 0)
            schedule.end    = new Date(2091, 0, 4, new_class.time_end[0], new_class.time_end[1], 0, 0)
            calendar.createSchedules([schedule])
          }
          if(new_class.days_of_week[4] == 1){
            schedule.id     = new_class.id
            schedule.start  = new Date(2091, 0, 5, new_class.time_start[0], new_class.time_start[1], 0, 0)
            schedule.end    = new Date(2091, 0, 5, new_class.time_end[0], new_class.time_end[1], 0, 0)
            calendar.createSchedules([schedule])
          }
          if(new_class.days_of_week[5] == 1){
            schedule.id     = new_class.id
            schedule.start  = new Date(2091, 0, 6, new_class.time_start[0], new_class.time_start[1], 0, 0)
            schedule.end    = new Date(2091, 0, 6, new_class.time_end[0], new_class.time_end[1], 0, 0)
            calendar.createSchedules([schedule])
          }
          if(new_class.days_of_week[6] == 1){
            schedule.id     = new_class.id
            schedule.start  = new Date(2091, 0, 7, new_class.time_start[0], new_class.time_start[1], 0, 0)
            schedule.end    = new Date(2091, 0, 7, new_class.time_end[0], new_class.time_end[1], 0, 0)
            calendar.createSchedules([schedule])
          }

        });
      },
      50
    );

  }

  // $scope.show_class = function (id, event) {
  //
  //   // only certain elements triggering 'ng-click' can trigger this function
  //   if (event){
  //     var allowed_targets = ['post-thumbnail-entry class-card', 'col', 'row', 'post-thumbnail-content']
  //     if (allowed_targets.some(v => event.target.className.includes(v))) {}
  //     else
  //       return
  //   }
  //
  //
  //   $scope.classes.forEach((_class, i) => {
  //     if(_class.id == id){
  //       if(_class.show_in_schedule == true) // if this class is already 'show', then toggle to hide
  //         _class.show_in_schedule = false
  //       else
  //         _class.show_in_schedule = true
  //     }
  //   });
  //
  //   $scope.save_classes()
  //
  //   $scope.populate_calendar();
  // }

  // $scope.hide_class = function (id) {
  //   $scope.classes.forEach((_class, i) => {
  //     if(_class.id == id){
  //       _class.show_in_schedule = false
  //     }
  //   });
  //
  //   $scope.save_classes()
  //
  //   $scope.populate_calendar()
  //
  // }

  $scope.toggle_class = function (_class, event){

    // only certain elements triggering 'ng-click' can trigger this function
    if (event){
      var allowed_targets = ['post-thumbnail-entry class-card', 'col', 'row', 'post-thumbnail-content']
      if (allowed_targets.some(v => event.target.className.includes(v))) {}
      else
        return
    }

    _class.show_in_schedule = !_class.show_in_schedule

    $scope.save_classes()

    $scope.populate_calendar()
  }

  $scope.show_class = function (_class){
      _class.show_in_schedule = true

      $scope.save_classes()

      $scope.populate_calendar()
  }

  $scope.hide_class = function (_class){
      _class.show_in_schedule = false

      $scope.save_classes()

      $scope.populate_calendar()
  }

  $scope.hide_class__id = function (_class_id){

      $scope.classes.forEach((_class, i) => {
        if(_class.id == _class_id){
          _class.show_in_schedule = false
        }
      });

      $scope.$apply()


      $scope.save_classes()

      $scope.populate_calendar()
  }

  $scope.create_class = function () {

    console.log($scope.classes);

    var new_class =
    {
      id:           Math.floor(Math.random() * 10001),
      show_in_schedule: true,
      name:         $scope.new_class__name,          //
      // professor:    $scope.new_class__professor,     //
      days_of_week: [
        $scope.new_class__day_of_week__monday ? 1 : 0,
        $scope.new_class__day_of_week__tuesday ? 1 : 0,
        $scope.new_class__day_of_week__wednesday ? 1 : 0,
        $scope.new_class__day_of_week__thursday ? 1 : 0,
        $scope.new_class__day_of_week__friday ? 1 : 0,
        $scope.new_class__day_of_week__saturday ? 1 : 0,
        $scope.new_class__day_of_week__sunday ? 1 : 0,
      ],  // 6 = sunday, 0 = monday, 5 = saturday
      time_start:   [$scope.new_class_time__start_hour, $scope.new_class_time__start_minute],
      time_end:     [$scope.new_class_time__end_hour, $scope.new_class_time__end_minute],
      // category:     $scope.new_class__category,      // Major/minor/ge...
      bgColor:      '#c0f3ff',
      bColor:       '#2cabdc'
    }

    $scope.classes.push(new_class)


    var schedule = {
          calendarId: '1',
          title: new_class.name,
          category: 'time',
      }

    if($scope.new_class__day_of_week__monday){
      schedule.id = new_class.id,
      schedule.start  = new Date(2091, 0, 1, new_class.time_start[0], new_class.time_start[1], 0, 0)
      schedule.end    = new Date(2091, 0, 1, new_class.time_end[0], new_class.time_end[1], 0, 0)
      calendar.createSchedules([schedule])
    }
    if($scope.new_class__day_of_week__tuesday){
      schedule.id = new_class.id,
      schedule.start  = new Date(2091, 0, 2, new_class.time_start[0], new_class.time_start[1], 0, 0)
      schedule.end    = new Date(2091, 0, 2, new_class.time_end[0], new_class.time_end[1], 0, 0)
      calendar.createSchedules([schedule])
    }
    if($scope.new_class__day_of_week__wednesday){
      schedule.id = new_class.id,
      schedule.start  = new Date(2091, 0, 3, new_class.time_start[0], new_class.time_start[1], 0, 0)
      schedule.end    = new Date(2091, 0, 3, new_class.time_end[0], new_class.time_end[1], 0, 0)
      calendar.createSchedules([schedule])
    }
    if($scope.new_class__day_of_week__thursday){
      schedule.id = new_class.id,
      schedule.start  = new Date(2091, 0, 4, new_class.time_start[0], new_class.time_start[1], 0, 0)
      schedule.end    = new Date(2091, 0, 4, new_class.time_end[0], new_class.time_end[1], 0, 0)
      calendar.createSchedules([schedule])
    }
    if($scope.new_class__day_of_week__friday){
      schedule.id = new_class.id,
      schedule.start  = new Date(2091, 0, 5, new_class.time_start[0], new_class.time_start[1], 0, 0)
      schedule.end    = new Date(2091, 0, 5, new_class.time_end[0], new_class.time_end[1], 0, 0)
      calendar.createSchedules([schedule])
    }
    if($scope.new_class__day_of_week__saturday){
      schedule.id = new_class.id,
      schedule.start  = new Date(2091, 0, 6, new_class.time_start[0], new_class.time_start[1], 0, 0)
      schedule.end    = new Date(2091, 0, 6, new_class.time_end[0], new_class.time_end[1], 0, 0)
      calendar.createSchedules([schedule])
    }
    if($scope.new_class__day_of_week__sunday){
      schedule.id = new_class.id,
      schedule.start  = new Date(2091, 0, 7, new_class.time_start[0], new_class.time_start[1], 0, 0)
      schedule.end    = new Date(2091, 0, 7, new_class.time_end[0], new_class.time_end[1], 0, 0)
      calendar.createSchedules([schedule])
    }

    $scope.save_classes()

  }

  $scope.delete_class = function (id) {

    if (!confirm("are you sure you want to delete this class?") )
      return

    $scope.classes = $scope.classes.filter(aClass => aClass.id !== id)

    $scope.save_classes()

    $scope.populate_calendar()
  }

  $scope.clear_classes = function () {
    if ( confirm('Are you sure you want to clear and delete all your classes?') ){
      $scope.classes = []
      $scope.save_classes()
      $scope.populate_calendar()
    }
  }

  $scope.update_schedule_time = function (id, date_start, date_end, date_old_start, date_old_end) {
    $scope.classes.forEach((_class, i) => {
      if(_class.id == id){

        // ======  change time  ======
        _class.time_start = [date_start.toDate().getHours(), date_start.toDate().getMinutes() ]
        _class.time_end = [date_end.toDate().getHours(), date_end.toDate().getMinutes() ]

        // ======  change day of week  ======
        var old_day_of_week = date_old_start.toDate().getDay() // return 0 - sun. 6 - sat
        old_day_of_week = old_day_of_week < 0 ? 7 : old_day_of_week - 1 // change to 0 - monday. 6 sunday

        var new_day_of_week = date_start.toDate().getDay() // return 0 - sun. 6 - sat
        new_day_of_week = new_day_of_week < 0 ? 7 : new_day_of_week - 1 // change to 0 - monday. 6 sunday

        _class.days_of_week[old_day_of_week] = 0
        _class.days_of_week[new_day_of_week] = 1
      }
    });

    $scope.$apply()
    $scope.save_classes()
    $scope.populate_calendar()
  }

  $scope.load_classes = function () {
    var class_json = $window.localStorage.getItem('classes')

    if (class_json == null || class_json == "" || class_json == "[]"){}
    else
      $scope.classes = JSON.parse(class_json)
  }

  $scope.save_classes = function () {
    var class_json = JSON.stringify($scope.classes)
    $window.localStorage.setItem('classes', class_json)
  }


}



