import { Component, OnInit } from '@angular/core';
import { TaskService } from 'src/app/Services/task.service';
import { Task } from 'src/app/Task';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.css']
})
export class ReportComponent implements OnInit {
  tasks: Task[] = [];
  students = [
    { id: 1, name: 'John Doe', marks: 95 },
    { id: 2, name: 'Jane Smith', marks: 88 },
    { id: 3, name: 'Alice Johnson', marks: 78 },
    { id: 4, name: 'Bob Anderson', marks: 92 },
    { id: 5, name: 'Eve Davis', marks: 85 },
    // Add more student data here
  ];

  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
    this.taskService.getTasks().subscribe((tasks) => (this.tasks = tasks));
  }

  deleteTask(task: Task) {
    this.taskService
      .deleteTask(task)
      .subscribe(
        () => (this.tasks = this.tasks.filter((t) => t.id !== task.id))
      );
  }

  // toggleReminder(task: Task) {
  //   task.reminder = !task.reminder;
  //   this.taskService.updateTaskReminder(task).subscribe();
  // }

}
