import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { HomeComponent } from './components/home/home.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {MatButtonModule} from "@angular/material/button";
import {MatInputModule} from "@angular/material/input";
import {MatIconModule} from "@angular/material/icon";
import { DashboardComponent } from './components/dashboard/dashboard.component';
import {MatSelectModule} from "@angular/material/select";
import { MatFormFieldModule } from "@angular/material/form-field";
import {MatCardModule} from "@angular/material/card";
import {MatListModule} from "@angular/material/list";
import { HttpClientModule } from '@angular/common/http';
import { ForgotPasswordComponent } from './components/forgot-password/forgot-password.component';
import { ConfirmEmailComponent } from './components/confirm-email/confirm-email.component';
import {MatToolbarModule} from "@angular/material/toolbar";




@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    HomeComponent,
    DashboardComponent,
    ForgotPasswordComponent,
    ConfirmEmailComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatInputModule,
    MatIconModule,
    MatSelectModule,
    MatFormFieldModule,
    MatCardModule,
    MatListModule,
    HttpClientModule,
    FormsModule,
    MatToolbarModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
