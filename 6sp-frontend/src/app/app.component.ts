import { Component, OnInit } from '@angular/core';
import { faUser } from '@fortawesome/free-solid-svg-icons';
import { Router } from '@angular/router';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = '6sp-frontend';
  userIcon;
  router1;
  showSpinner:boolean = false;

  constructor(public router: Router){
    this.userIcon = faUser
    this.router1 = router
  }

  subscribeToChildEmitter(componentRef:any){
    componentRef.loadSpinnerEvent.subscribe((res:boolean)=>{
        this.showSpinner = res
    })
  }

  ngOnInit(): void {

  }
}
