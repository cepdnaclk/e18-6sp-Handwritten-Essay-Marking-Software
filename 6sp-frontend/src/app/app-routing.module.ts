import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './Components/home/home.component';
import { ReportComponent } from './Components/report/report.component';
import { RegisterComponent } from './Components/register/register.component';
import { LoginComponent } from './Components/login/login.component';
import { IntroComponent } from './Components/intro/intro.component';
import { AppComponent } from './app.component';

const routes: Routes = [
  
  {path: 'login', component:LoginComponent},
  {path: 'home', component:HomeComponent},
  {path: 'report', component:ReportComponent},
  {path: 'register', component:RegisterComponent},
  {path: '', component:IntroComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
