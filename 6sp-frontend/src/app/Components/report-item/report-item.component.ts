import { Component, OnInit,EventEmitter,Input,Output } from '@angular/core';
import { Task } from '../../Task';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-report-item',
  templateUrl: './report-item.component.html',
  styleUrls: ['./report-item.component.css']
})
export class ReportItemComponent implements OnInit {
  @Input() task!: Task;
  @Input() studentNumber!: number;
  @Output() onDeleteTask: EventEmitter<Task> = new EventEmitter();
  @Output() onToggleReminder: EventEmitter<Task> = new EventEmitter();
  faTimes = faTimes;
  // students = [
  //   { id: 1, name: 'John Doe', marks: 95 },
  //   { id: 2, name: 'Jane Smith', marks: 88 },
  //   { id: 3, name: 'Alice Johnson', marks: 78 },
  //   { id: 4, name: 'Bob Anderson', marks: 92 },
  //   { id: 5, name: 'Eve Davis', marks: 85 },
  //   // Add more student data here
  // ];

  constructor() {}

  ngOnInit(): void {}

  onDelete(task:Task) {
    this.onDeleteTask.emit(task);
  }

  onToggle(task:Task) {
    this.onToggleReminder.emit(task);
  }
}
