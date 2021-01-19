import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FormGroup, FormBuilder, Validators, AbstractControl, ValidationErrors } from '@angular/forms';

import { LoginInfo } from 'src/app/shared/models/shared.models';
import { ApiService } from 'src/app/shared/services/api.service';
import { LoginService } from 'src/app/shared/services/login.service';
import { environment } from 'src/environments/environment';

import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'login-register',
  templateUrl: './login-register.component.html',
  styleUrls: ['./login-register.component.scss']
})
export class LoginRegisterComponent implements OnInit {
  loginForm: FormGroup;
  registerForm: FormGroup;
  loginFormSubmitted: Boolean = false;
  registerFormSubmitted: Boolean = false;
  registerPageVisible: Boolean = false;

  constructor(private formBuilder: FormBuilder,
              private apiService: ApiService,
              private toastr: ToastrService,
              private loginService: LoginService,
              private router: Router) { }

  ngOnInit(): void {
    this.buildLoginForm();
    this.buildRegisterForm();
  }

  get loginControls() { return this.loginForm.controls; }

  get registerControls() { return this.registerForm.controls; }

  private buildLoginForm() {
      this.loginForm = this.formBuilder.group({
          email: ['', [Validators.required, Validators.email]],
          password: ['', [Validators.required, Validators.minLength(6)]]
      });
  }

  private buildRegisterForm() {
      this.registerForm = this.formBuilder.group({
        email: ['', [Validators.required, Validators.email]],
        password: ['', [Validators.required, Validators.minLength(6)]],
        repeatPassword: ['', [Validators.required, LoginRegisterComponent.matchValues('password') ]]
      });
  }

  public static matchValues(matchTo: string): (AbstractControl) => ValidationErrors | null {
    return (control: AbstractControl): ValidationErrors | null => {
      return !!control.parent &&
        !!control.parent.value &&
        control.value === control.parent.controls[matchTo].value
        ? null
        : { isMatching: false };
    };
  }

  public toggleRegisterPage(registerPageVisible) {
    if(registerPageVisible) {
      if(this.registerPageVisible)
        return;

      this.registerPageVisible = true;
      this.registerFormSubmitted = false;
      this.clearForm(this.registerControls);
      document.querySelector(".container").classList.add("active");
    }
    else {
      this.registerPageVisible = false;
      this.loginFormSubmitted = false;
      this.clearForm(this.loginControls);
      document.querySelector(".container").classList.remove("active");
    }
  } 

  submitLoginForm() {
    this.loginFormSubmitted = true;

    if (this.loginForm.invalid)
      return;

    this.loginFormSubmitted = false;

    var loginInfo: LoginInfo = this.createLoginInfo(this.loginForm);

    this.apiService.login(loginInfo).subscribe(
      (response) => {
        if(response.error !== "" || response.code === "404") {
          this.clearForm(this.loginControls);
          this.errorToast(response.error);
        } else {
          this.loginService.saveLoggedInUser(response.userID, loginInfo.Email);
          environment.hideLandingPage = true;
          this.router.navigate(['']);
        }
      },
      _ => {
        this.clearForm(this.loginControls);
        this.errorToast("An error has occured");
    });
  }

  submitRegisterForm() {
    this.registerFormSubmitted = true;

    if (this.registerForm.invalid)
      return;

    this.registerFormSubmitted = false;

    var loginInfo: LoginInfo = this.createLoginInfo(this.registerForm);

    this.apiService.register(loginInfo).subscribe(
      (response) => {
        if(response.error !== "" || response.code === "404") {
          this.clearForm(this.registerControls);
          this.errorToast(response.error);
        } else {
          this.successToast("Successfully registered!");
          this.toggleRegisterPage(false);
        }
      },
      _ => {
        this.clearForm(this.registerControls);
        this.errorToast("An error has occured");
    });
  }

  private createLoginInfo(form: FormGroup): LoginInfo {
    var loginInfo: LoginInfo = new LoginInfo();

    loginInfo.Email = form.controls["email"].value;
    loginInfo.Password = form.controls["password"].value;

    return loginInfo;
  }
  
  private clearForm(controls: { [key: string]: AbstractControl; }) {
    Object.values(controls).forEach(control => control.setValue(""));
  }

  private errorToast(message) {
    this.toastr.error(message,'', {
      timeOut: 1500,
    });
  }

  private successToast(message) {
    this.toastr.success(message,'', {
      timeOut: 1500,
    });
  }
}