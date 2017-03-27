subroutine calcMomentum(freq, phase, gamma_start, dz, gamma_tilde_dash, t, gamma_dash, gamma, beta, p)
  implicit none
  real(8), parameter :: pi = 4.0 * atan(1.0)
  real(8), parameter :: c = 299792458.0

  real(8), intent(in)  :: freq
  real(8), intent(in)  :: phase
  real(8), intent(in)  :: gamma_start
  real(8), intent(in)  :: dz
  real(8), intent(in)  :: gamma_tilde_dash(:)

  real(8), intent(out) :: t(size(gamma_tilde_dash,1))
  real(8), intent(out) :: gamma_dash(size(gamma_tilde_dash,1))
  real(8), intent(out) :: gamma(size(gamma_tilde_dash,1))
  real(8), intent(out) :: beta(size(gamma_tilde_dash,1))
  real(8), intent(out) :: p(size(gamma_tilde_dash,1))

  real(8) :: omega
  real(8) :: dt
  integer i

  omega = 2 * pi * freq
  gamma(1) = gamma_start
  beta(1) = sqrt(1.0 - 1.0 / gamma(1) ** 2.0)
  p(1) = gamma(1) * beta(1)
  t(1) = phase / (360.0 * freq)

  do i = 1, size(gamma_tilde_dash,1) - 1
    gamma_dash(i) = gamma_tilde_dash(i) * cos(omega * t(i))
    gamma(i+1) = gamma(i) + gamma_dash(i) * dz
    p(i+1) = sqrt(gamma(i+1) ** 2.0 - 1.0)
    beta(i+1) = p(i+1) / gamma(i+1)
    if (gamma_dash(i) .eq. 0) then
      dt = 1 / (beta(i) * c)
    else
      dt = (p(i+1) - p(i)) / (gamma_dash(i) * c)
    end if
    t(i+1) = t(i) + dt
  end do
end subroutine
