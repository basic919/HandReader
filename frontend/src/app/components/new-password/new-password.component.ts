import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {Router, ActivatedRoute} from "@angular/router";
import {AuthResponse} from "../../models/auth-response";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../../environments/environment";
import {logMessages} from "@angular-devkit/build-angular/src/builders/browser-esbuild/esbuild";

@Component({
  selector: 'app-new-password',
  templateUrl: './new-password.component.html',
  styleUrls: ['./new-password.component.less']
})
export class NewPasswordComponent implements OnInit {

  newPasswordUrl = environment.apiUrl + "/user/new_password"

  newPasswordForm: FormGroup = new FormGroup({});

  token = "";

  constructor(private formBuilder: FormBuilder, private router: Router, private httpClient: HttpClient, private route: ActivatedRoute) { }

  ngOnInit(): void {

    this.newPasswordForm = this.formBuilder.group({
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    });

    this.token = this.route.snapshot.params['token'];
  }

  onSubmit() {
    this.httpClient.post<AuthResponse>(this.newPasswordUrl,
      {"new_password": this.newPasswordForm.get("password")?.value},
      {params: {token: this.token}}).subscribe(
        (data: AuthResponse)=>{
        if(data.value){
          console.log(data.message);
          this.router.navigate(['/login']);
      }
    });
  }

}
