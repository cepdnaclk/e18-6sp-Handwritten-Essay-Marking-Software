import { Component,ViewChild,ElementRef, Output,EventEmitter} from '@angular/core';
import { Task } from 'src/app/Task';
import { TaskService } from 'src/app/Services/task.service';  

const newTask: Task = {
  name: "",
  email: "",
  marks: 0
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  name: string = '';
  email: string = '';
  marks: Number = 0;
  selectedFile: File | null = null;
  @ViewChild('fileInput') fileInput!: ElementRef;
  @Output() loadSpinnerEvent: EventEmitter<Boolean> = new EventEmitter();

  constructor(private taskService:TaskService) {}

  onFileChange(event: any) {
    const files: FileList = event.target.files;
    if (files.length > 0) {
      this.selectedFile = files[0];
    } else {
      this.selectedFile = null;
    }
  }

  randomIntFromInterval(min:number, max:number):number { // min and max included 
    return Math.floor(Math.random() * (max - min + 1) + min)
  }
  

  uploadFile() {
    if (!this.selectedFile) {
      console.error('No file selected.');
      return;
    }

    // Perform file upload logic here (e.g., send the file to a server)

    // Reset the file input
    if (this.fileInput) {
      this.fileInput.nativeElement.value = '';
    }

    console.log('File uploaded:', this.selectedFile);
  }

  clearScreen(){
    this.name = ''
    this.email = ''
  }

  async onSubmit(){
    const rndInt = this.randomIntFromInterval(60, 100)
    newTask.name = this.name;
    newTask.email = this.email;
    newTask.marks = rndInt;
    console.log(rndInt);

    this.marks = rndInt;
    // this.loadSpinnerEvent.emit(true);
    // await new Promise(f => setTimeout(f, 3500));
    
    // this.loadSpinnerEvent.emit(false);

    this.taskService.addTask(newTask).subscribe((task) => newTask);
    
    this.clearScreen()
    

  }

}
